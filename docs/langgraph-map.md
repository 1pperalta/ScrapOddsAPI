## LangGraph Agent Map

This diagram describes the current control flow implemented in `odds-agent/backend/server_py/graph.py`.

```mermaid
flowchart TD
  U[User query] --> A[Node: agent (LLM)]
  A -->|tool_calls exist AND below max tool iterations| T[Node: tools (execute tool calls)]
  T --> A
  A -->|no tool_calls OR max tool iterations reached| R[END (return LLM final message)]

  subgraph Agent Internals
    A1[agent: check_budget before LLM call] --> A2[LLM invoke with system prompt + messages]
    A2 --> A3[record token usage to BudgetTracker]
  end
```

