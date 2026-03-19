from langchain_core.tools import tool
from server_py.services.rag_service import get_rag_service


@tool
def get_team_context(team_name: str) -> str:
    """Retrieve contextual information about a football team from the knowledge base.
    Returns recent form, league position, and performance data.
    Use this to enrich analysis with historical and statistical context."""
    rag_service = get_rag_service()
    contexts = rag_service.retrieve_team_context(team_name, top_k=2)

    if not contexts:
        return f"No context available for '{team_name}' in the knowledge base."

    return rag_service.format_context_for_prompt(contexts)
