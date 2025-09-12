import httpx
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")  
SPORT = "soccer_epl"       # English Premier League
REGIONS_TO_TRY = ["us", "uk", "au", "eu"]  #
MARKETS = "h2h"            # "h2h" = Match Winner (Home/Draw/Away)

# Function to test a region
def test_region(region):
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": region,
        "markets": MARKETS,
        "oddsFormat": "decimal"
    }
    
    print(f"\n🔄 Testing region: {region}")
    try:
        r = httpx.get(url, params=params, timeout=30.0)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Success! Found {len(data)} games")
            if data:
                # Show sample bookmakers from this region
                bookmakers = set()
                for game in data[:1]:  # Just check first game
                    for book in game.get("bookmakers", []):
                        bookmakers.add(book["title"])
                print(f"Sample bookmakers: {list(bookmakers)[:5]}")
            return data
        else:
            print(f"❌ Failed: {r.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Test all regions
print(f"API Key loaded: {'Yes' if API_KEY else 'No'}")
all_data = []

for region in REGIONS_TO_TRY:
    data = test_region(region)
    if data:
        # Add region info to each game
        for game in data:
            game["source_region"] = region
        all_data.extend(data)

# Check all unique bookmakers across all regions
all_bookmakers = set()
for game in all_data:
    for book in game.get("bookmakers", []):
        all_bookmakers.add(book["title"])

print(f"\n📊 All bookmakers found across regions:")
for bookie in sorted(all_bookmakers):
    print(f"  - {bookie}")
    
# Check for Colombian or Latin American bookmakers
colombian_keywords = ["colombia", "latin", "betplay", "wplay", "rushbet"]
potential_colombian = [b for b in all_bookmakers if any(keyword.lower() in b.lower() for keyword in colombian_keywords)]
if potential_colombian:
    print(f"\n🇨🇴 Potential Colombian/Latin American bookmakers found: {potential_colombian}")
else:
    print(f"\n❌ No obvious Colombian bookmakers found in current regions")

# 2. Flatten data into a nice table
rows = []
for game in all_data:  # Fixed: using all_data instead of data
    home = game["home_team"]
    away = game["away_team"]
    commence = game["commence_time"]   # kickoff time
    region = game.get("source_region", "unknown")

    for book in game["bookmakers"]:
        bookie = book["title"]
        for market in book["markets"]:
            for outcome in market["outcomes"]:
                rows.append({
                    "home": home,
                    "away": away,
                    "kickoff": commence,
                    "region": region,
                    "bookmaker": bookie,
                    "outcome": outcome["name"],   # Home / Draw / Away
                    "odds": outcome["price"]
                })

df = pd.DataFrame(rows)

df.to_csv("premier_league_odds_all_regions.csv", index=False)
print(f"✅ Saved {len(rows)} odds records to premier_league_odds_all_regions.csv")

# Show bookmakers by region
if rows:
    print(f"\n🌍 Bookmakers by region:")
    region_bookmakers = df.groupby('region')['bookmaker'].unique()
    for region, bookies in region_bookmakers.items():
        print(f"{region}: {list(bookies)[:3]}..." if len(bookies) > 3 else f"{region}: {list(bookies)}")
