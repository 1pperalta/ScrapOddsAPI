import httpx
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")  
SPORT = "soccer_epl"       # English Premier League
REGION = "uk"              # Odds from UK bookmakers
MARKETS = "h2h"            # "h2h" = Match Winner (Home/Draw/Away)

url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

params = {
    "apiKey": API_KEY,
    "regions": REGION,      # bookmakers region
    "markets": MARKETS,     # what type of odds
    "oddsFormat": "decimal" # easier than American odds
}

# 1. Call the API
r = httpx.get(url, params=params, timeout=30.0)
r.raise_for_status()
data = r.json()

# 2. Flatten data into a nice table
rows = []
for game in data:
    home = game["home_team"]
    away = game["away_team"]
    commence = game["commence_time"]   # kickoff time

    for book in game["bookmakers"]:
        bookie = book["title"]
        for market in book["markets"]:
            for outcome in market["outcomes"]:
                rows.append({
                    "home": home,
                    "away": away,
                    "kickoff": commence,
                    "bookmaker": bookie,
                    "outcome": outcome["name"],   # Home / Draw / Away
                    "odds": outcome["price"]
                })

df = pd.DataFrame(rows)

df.to_csv("premier_league_odds.csv", index=False)
print("✅ Saved odds to premier_league_odds.csv")
