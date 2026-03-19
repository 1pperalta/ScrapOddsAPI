import json
from langchain_core.tools import tool
from server_py.services.odds_service import LiveOddsService


def _format_odds(odds: dict) -> str:
    lines = []
    for outcome, data in odds.items():
        bookmakers = ", ".join(
            f"{bm['bookmaker']}: {bm['price']}" for bm in data["all_bookmakers"]
        )
        lines.append(
            f"  {outcome}: best {data['best_price']} ({data['best_bookmaker']}) | all: [{bookmakers}]"
        )
    return "\n".join(lines)


def _format_match(match: dict) -> str:
    header = (
        f"{match['home_team']} vs {match['away_team']}\n"
        f"  League: {match['league']}\n"
        f"  Kickoff: {match['kickoff']}"
    )
    if match.get("odds"):
        return f"{header}\n{_format_odds(match['odds'])}"
    return f"{header}\n  No odds available"


@tool
def search_team_odds(team_name: str) -> str:
    """Search upcoming matches and betting odds for a specific football team.
    Returns match details and odds from multiple bookmakers.
    Use this when the user asks about a team's upcoming games, odds, or analysis."""
    service = LiveOddsService()
    try:
        matches = service.get_upcoming_matches_for_team(team_name, limit=3)
    finally:
        service.close()

    if not matches:
        return f"No upcoming matches found for '{team_name}' in the database."

    parts = [f"Upcoming matches for {team_name} ({len(matches)} found):\n"]
    for i, match in enumerate(matches, 1):
        parts.append(f"Match {i}: {_format_match(match)}")
    return "\n\n".join(parts)


@tool
def search_match_odds(home_team: str, away_team: str) -> str:
    """Search betting odds for a specific match between two teams.
    Returns detailed odds from all bookmakers for the match.
    Use this when the user asks about a specific matchup like 'Arsenal vs Chelsea'."""
    service = LiveOddsService()
    try:
        match_data = service.get_match_analysis_data(home_team, away_team)
        if not match_data:
            match_data = service.get_match_analysis_data(away_team, home_team)
    finally:
        service.close()

    if not match_data:
        return f"No upcoming match found between '{home_team}' and '{away_team}'."

    return _format_match(match_data)


@tool
def get_league_matches(league: str) -> str:
    """Get all upcoming matches and odds for a specific league.
    Supported leagues: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Champions League.
    Use this when the user asks about value bets or best odds in a league."""
    service = LiveOddsService()
    try:
        matches = service.get_all_upcoming_matches(league=league, limit=5)
    finally:
        service.close()

    if not matches:
        return (
            f"No upcoming matches found for '{league}'. "
            "Available leagues: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Champions League."
        )

    parts = [f"Upcoming matches in {league} ({len(matches)} found):\n"]
    for i, match in enumerate(matches, 1):
        parts.append(f"Match {i}: {_format_match(match)}")
    return "\n\n".join(parts)
