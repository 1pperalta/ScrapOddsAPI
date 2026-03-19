from server_py.tools.odds_tools import search_team_odds, search_match_odds, get_league_matches
from server_py.tools.rag_tools import get_team_context
from server_py.tools.football_data_tools import get_standings, get_top_scorers

ALL_TOOLS = [
    search_team_odds,
    search_match_odds,
    get_league_matches,
    get_team_context,
    get_standings,
    get_top_scorers,
]
