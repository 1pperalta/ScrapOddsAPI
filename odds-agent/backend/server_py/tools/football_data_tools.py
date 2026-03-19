import os
import httpx
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"

LEAGUE_CODES = {
    "premier league": "PL",
    "la liga": "PD",
    "serie a": "SA",
    "bundesliga": "BL1",
    "ligue 1": "FL1",
    "champions league": "CL",
}


def _get_headers() -> dict:
    return {"X-Auth-Token": os.getenv("FOOTBALL_DATA_API_KEY", "")}


def _resolve_league_code(league: str) -> str | None:
    normalized = league.strip().lower()
    if normalized in LEAGUE_CODES:
        return LEAGUE_CODES[normalized]
    for name, code in LEAGUE_CODES.items():
        if normalized in name or name in normalized:
            return code
    if league.upper() in LEAGUE_CODES.values():
        return league.upper()
    return None


@tool
def get_standings(league: str) -> str:
    """Get the current league table / standings for a football league.
    Accepts league names like 'Premier League', 'La Liga', 'Serie A',
    'Bundesliga', 'Ligue 1', 'Champions League', or codes like 'PL', 'PD'.
    Use this when the user asks about league positions, table, or standings."""
    code = _resolve_league_code(league)
    if not code:
        return (
            f"Unknown league '{league}'. "
            f"Supported: {', '.join(LEAGUE_CODES.keys())}"
        )

    try:
        response = httpx.get(
            f"{BASE_URL}/competitions/{code}/standings",
            headers=_get_headers(),
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return f"API error fetching standings for {league}: {e.response.status_code}"
    except httpx.RequestError as e:
        return f"Network error fetching standings: {e}"

    data = response.json()
    standings = data.get("standings", [])
    if not standings:
        return f"No standings data available for {league}."

    total_table = standings[0].get("table", [])
    lines = [f"Standings for {data.get('competition', {}).get('name', league)}:\n"]
    lines.append(f"{'Pos':<4} {'Team':<25} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GD':>4} {'Pts':>4}")
    lines.append("-" * 52)

    for entry in total_table[:20]:
        team = entry.get("team", {}).get("name", "?")
        lines.append(
            f"{entry['position']:<4} {team:<25} "
            f"{entry['playedGames']:>3} {entry['won']:>3} "
            f"{entry['draw']:>3} {entry['lost']:>3} "
            f"{entry['goalDifference']:>4} {entry['points']:>4}"
        )

    return "\n".join(lines)


@tool
def get_top_scorers(league: str) -> str:
    """Get the top scorers for a football league.
    Accepts league names like 'Premier League', 'La Liga', etc.
    Use this when the user asks about top scorers or goal statistics."""
    code = _resolve_league_code(league)
    if not code:
        return (
            f"Unknown league '{league}'. "
            f"Supported: {', '.join(LEAGUE_CODES.keys())}"
        )

    try:
        response = httpx.get(
            f"{BASE_URL}/competitions/{code}/scorers",
            headers=_get_headers(),
            params={"limit": 10},
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return f"API error fetching scorers for {league}: {e.response.status_code}"
    except httpx.RequestError as e:
        return f"Network error fetching scorers: {e}"

    data = response.json()
    scorers = data.get("scorers", [])
    if not scorers:
        return f"No scorers data available for {league}."

    lines = [f"Top scorers in {data.get('competition', {}).get('name', league)}:\n"]
    for i, entry in enumerate(scorers, 1):
        player = entry.get("player", {})
        team = entry.get("team", {}).get("name", "?")
        goals = entry.get("goals", 0)
        assists = entry.get("assists", 0) or 0
        lines.append(
            f"{i}. {player.get('name', '?')} ({team}) - "
            f"{goals} goals, {assists} assists"
        )

    return "\n".join(lines)
