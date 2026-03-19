import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END

from server_py.tools import ALL_TOOLS
from server_py.budget import get_budget_tracker, BudgetExhaustedError

load_dotenv()

SYSTEM_PROMPT = """You are a professional football and sports betting analyst.

SCOPE:
- You ONLY answer questions about football (soccer) and sports betting.
- If a query is unrelated to football or betting, politely decline and suggest a football-related question.

RULES:
1. Only reference data returned by your tools. Never invent matches, odds, or statistics.
2. When analyzing a team, always call search_team_odds and get_team_context for complete data.
3. When analyzing a match, always call search_match_odds and get_team_context for both teams.
4. For value bets or league overviews, call get_league_matches and optionally get_standings.
5. Keep responses under 200 words. Be direct and professional.
6. Use clean markdown formatting with headings starting with "##".
7. Do not use emojis anywhere in the output.
8. Respond in the same language the user writes in.
9. Output template (use only the sections that make sense for the query, but keep the headings):
   - ## Resumen
   - ## Mejores Opciones
   - ## Justificacion
   - ## Datos Usados
10. "Mejores Opciones" should be a short list (max 3 items) using either "-" bullets or numbered "1." items.
11. "Datos Usados" must mention which tool(s) you relied on (e.g., "search_team_odds", "get_team_context").

AVAILABLE DATA:
- Live betting odds from multiple bookmakers (via search_team_odds, search_match_odds, get_league_matches)
- Team context: form, standings, recent results (via get_team_context)
- Live league tables (via get_standings)
- Top scorers (via get_top_scorers)"""

MAX_TOOL_ITERATIONS = 3


def _build_llm() -> ChatOpenAI:
    tracker = get_budget_tracker()
    return ChatOpenAI(
        model="deepseek/deepseek-chat-v3.1",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
        max_tokens=tracker.max_output_tokens,
        temperature=0.4,
    )


def _make_llm_node(llm_with_tools):
    def llm_node(state: MessagesState):
        tracker = get_budget_tracker()
        tracker.check_budget()

        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

        response = llm_with_tools.invoke(messages)

        usage = response.response_metadata.get("token_usage") or response.response_metadata.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        if input_tokens or output_tokens:
            tracker.record_usage(input_tokens, output_tokens)

        return {"messages": [response]}

    return llm_node


def _tool_node(state: MessagesState):
    tools_by_name = {t.name: t for t in ALL_TOOLS}
    last_message = state["messages"][-1]
    results = []
    for call in last_message.tool_calls:
        tool = tools_by_name.get(call["name"])
        if tool is None:
            results.append(
                ToolMessage(
                    content=f"Unknown tool: {call['name']}",
                    tool_call_id=call["id"],
                )
            )
            continue
        try:
            output = tool.invoke(call["args"])
        except Exception as e:
            output = f"Tool error: {e}"
        results.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
    return {"messages": results}


def _should_continue(state: MessagesState):
    last_message = state["messages"][-1]

    tool_call_count = sum(1 for m in state["messages"] if isinstance(m, ToolMessage))
    if tool_call_count >= MAX_TOOL_ITERATIONS * len(ALL_TOOLS):
        return END

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


def build_graph():
    llm = _build_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    graph = StateGraph(MessagesState)
    graph.add_node("agent", _make_llm_node(llm_with_tools))
    graph.add_node("tools", _tool_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", _should_continue, ["tools", END])
    graph.add_edge("tools", "agent")

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def invoke_agent(query: str) -> str:
    graph = get_graph()
    try:
        result = graph.invoke({"messages": [HumanMessage(content=query)]})
        last_message = result["messages"][-1]
        return last_message.content
    except BudgetExhaustedError as e:
        return f"## Budget Limit Reached\n\n{str(e)}\n\nPlease contact the administrator."
    except Exception as e:
        return f"## Error\n\nFailed to process query: {str(e)}"
