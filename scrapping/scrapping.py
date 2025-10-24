import httpx
from dotenv import load_dotenv
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import time
import random

# Load environment variables from project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))

API_KEY = os.getenv("ODDS_API_KEY")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "betting_odds")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Debug environment variables
print("=== ENVIRONMENT VARIABLES DEBUG ===")
print(f"API_KEY: {'***' + API_KEY[-4:] if API_KEY else 'NOT FOUND'}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {'***' if DB_PASSWORD else 'NOT FOUND'}")
print(f".env file path: {os.path.join(os.path.dirname(__file__), '.env')}")
print(f".env file exists: {os.path.exists(os.path.join(os.path.dirname(__file__), '.env'))}")
print("=" * 40)

# Top 5 European leagues + Champions League
LEAGUES = {
    "Premier League": "soccer_epl",
    "La Liga": "soccer_spain_la_liga",
    "Serie A": "soccer_italy_serie_a",
    "Bundesliga": "soccer_germany_bundesliga",
    "Ligue 1": "soccer_france_ligue_one",
    "Champions League": "soccer_uefa_champs_league",
}

REGIONS = ["us", "uk", "au", "eu"]
MARKETS = "h2h"

def test_api_connection():
    """Test if API key is working"""
    print("\n=== TESTING API CONNECTION ===")
    if not API_KEY:
        print("❌ API_KEY not found!")
        return False
    
    try:
        # Test with sports endpoint first
        url = "https://api.the-odds-api.com/v4/sports"
        params = {"apiKey": API_KEY}
        
        print(f"Testing URL: {url}")
        print(f"API Key (last 4 chars): ***{API_KEY[-4:]}")
        
        r = httpx.get(url, params=params, timeout=30.0)
        
        print(f"Response Status: {r.status_code}")
        print(f"Response Headers: {dict(r.headers)}")
        
        if r.status_code == 200:
            sports = r.json()
            print(f"✅ API working! Found {len(sports)} sports")
            
            # Show available sports for debugging
            print("\nAvailable sports:")
            for sport in sports[:10]:  # Show first 10
                print(f"  - {sport.get('key', 'N/A')}: {sport.get('title', 'N/A')}")
            if len(sports) > 10:
                print(f"  ... and {len(sports) - 10} more")
            
            return True
        elif r.status_code == 401:
            print("❌ Invalid API key (401 Unauthorized)")
            print(f"Response: {r.text}")
            return False
        elif r.status_code == 429:
            print("❌ Rate limited (429)")
            print(f"Response: {r.text}")
            return False
        else:
            print(f"❌ API error: {r.status_code}")
            print(f"Response: {r.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_database_connection():
    """Test if database connection is working"""
    print("\n=== TESTING DATABASE CONNECTION ===")
    if not DB_PASSWORD:
        print("❌ DB_PASSWORD not found!")
        return False
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Database connected! PostgreSQL version: {version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def init_database():
    """Create database schema if it doesn't exist"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            api_key VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            league_id INTEGER REFERENCES leagues(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, league_id)
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookmakers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            region VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            league_id INTEGER REFERENCES leagues(id),
            home_team_id INTEGER REFERENCES teams(id),
            away_team_id INTEGER REFERENCES teams(id),
            kickoff TIMESTAMP NOT NULL,
            api_match_id VARCHAR(100) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS odds (
            id SERIAL PRIMARY KEY,
            match_id INTEGER REFERENCES matches(id),
            bookmaker_id INTEGER REFERENCES bookmakers(id),
            outcome VARCHAR(20) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(match_id, bookmaker_id, outcome, collected_at)
        );
    """)
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_odds_match ON odds(match_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_odds_collected ON odds(collected_at);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_matches_kickoff ON matches(kickoff);")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database schema initialized")

def get_or_create_league(cur, name, api_key):
    """Get league ID or create if doesn't exist"""
    cur.execute("SELECT id FROM leagues WHERE api_key = %s", (api_key,))
    result = cur.fetchone()
    if result:
        return result[0]
    
    cur.execute(
        "INSERT INTO leagues (name, api_key) VALUES (%s, %s) RETURNING id",
        (name, api_key)
    )
    return cur.fetchone()[0]

def get_or_create_team(cur, name, league_id):
    """Get team ID or create if doesn't exist"""
    cur.execute("SELECT id FROM teams WHERE name = %s AND league_id = %s", (name, league_id))
    result = cur.fetchone()
    if result:
        return result[0]
    
    cur.execute(
        "INSERT INTO teams (name, league_id) VALUES (%s, %s) RETURNING id",
        (name, league_id)
    )
    return cur.fetchone()[0]

def get_or_create_bookmaker(cur, name, region):
    """Get bookmaker ID or create if doesn't exist"""
    cur.execute("SELECT id FROM bookmakers WHERE name = %s", (name,))
    result = cur.fetchone()
    if result:
        return result[0]
    
    cur.execute(
        "INSERT INTO bookmakers (name, region) VALUES (%s, %s) RETURNING id",
        (name, region)
    )
    return cur.fetchone()[0]

def fetch_league_odds(league_name, sport_key):
    """Fetch odds for a specific league with improved error handling"""
    print(f"\n{'='*60}")
    print(f"Fetching: {league_name}")
    print(f"{'='*60}")
    
    all_games = []
    
    for region in REGIONS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": region,
            "markets": MARKETS,
            "oddsFormat": "decimal"
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"  {region}: Attempt {attempt + 1}")
                
                # Create a new client for each request with longer timeout
                with httpx.Client(timeout=60.0) as client:
                    r = client.get(url, params=params)
                
                print(f"  {region}: Response status: {r.status_code}")
                
                if r.status_code == 200:
                    data = r.json()
                    
                    if data:
                        for game in data:
                            game["league"] = league_name
                            game["sport_key"] = sport_key
                            game["source_region"] = region
                        all_games.extend(data)
                        print(f"  {region}: ✅ {len(data)} matches")
                    else:
                        print(f"  {region}: ⚠️  No matches found")
                    break  # Success, exit retry loop
                    
                elif r.status_code == 429:
                    print(f"  {region}: ⏰ Rate limited (429)")
                    print(f"  {region}: Response: {r.text}")
                    if attempt < max_retries - 1:
                        wait_time = 60 + (attempt * 30)  # Increase wait time with each attempt
                        print(f"  {region}: Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"  {region}: ❌ Failed after {max_retries} attempts")
                        
                elif r.status_code == 401:
                    print(f"  {region}: ❌ Unauthorized (401) - Check API key")
                    print(f"  Response: {r.text}")
                    break
                    
                elif r.status_code == 404:
                    print(f"  {region}: ❌ Not found (404) - Sport key might be invalid")
                    print(f"  Response: {r.text}")
                    break
                    
                else:
                    print(f"  {region}: ❌ Failed ({r.status_code})")
                    print(f"  Response: {r.text}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    break
                    
            except httpx.ConnectError as e:
                print(f"  {region}: 🔌 Connection error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    wait_time = 5 + random.uniform(1, 5)
                    print(f"  {region}: Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"  {region}: ❌ Failed after {max_retries} connection attempts")
                    
            except httpx.TimeoutException as e:
                print(f"  {region}: ⏱️  Timeout error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"  {region}: Retrying...")
                    time.sleep(10)
                    continue
                else:
                    print(f"  {region}: ❌ Failed after {max_retries} timeout attempts")
                    
            except Exception as e:
                print(f"  {region}: ❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    print(f"  {region}: ❌ Failed after {max_retries} attempts")
        
        # Add delay between regions to be respectful to the API
        if region != REGIONS[-1]:  # Don't wait after the last region
            print(f"  Waiting 3 seconds before next region...")
            time.sleep(3)
    
    return all_games

def save_to_database(all_data):
    """Save fetched odds to PostgreSQL database"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    stats = {
        "matches": 0,
        "odds_records": 0,
        "new_teams": 0,
        "new_bookmakers": 0
    }
    
    collected_at = datetime.now()
    
    for game in all_data:
        try:
            league_id = get_or_create_league(cur, game["league"], game["sport_key"])
            
            home_team_id = get_or_create_team(cur, game["home_team"], league_id)
            away_team_id = get_or_create_team(cur, game["away_team"], league_id)
            
            kickoff = datetime.fromisoformat(game["commence_time"].replace('Z', '+00:00'))
            api_match_id = game.get("id", f"{game['home_team']}_{game['away_team']}_{kickoff}")
            
            cur.execute("""
                INSERT INTO matches (league_id, home_team_id, away_team_id, kickoff, api_match_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (api_match_id) DO UPDATE SET kickoff = EXCLUDED.kickoff
                RETURNING id
            """, (league_id, home_team_id, away_team_id, kickoff, api_match_id))
            
            match_id = cur.fetchone()[0]
            stats["matches"] += 1
            
            for bookmaker in game.get("bookmakers", []):
                bookmaker_id = get_or_create_bookmaker(
                    cur, 
                    bookmaker["title"], 
                    game["source_region"]
                )
                
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        try:
                            cur.execute("""
                                INSERT INTO odds (match_id, bookmaker_id, outcome, price, collected_at)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT DO NOTHING
                            """, (
                                match_id,
                                bookmaker_id,
                                outcome["name"],
                                outcome["price"],
                                collected_at
                            ))
                            stats["odds_records"] += 1
                        except Exception as e:
                            print(f"Error inserting odds: {e}")
                            continue
            
            conn.commit()
            
        except Exception as e:
            print(f"Error processing game: {e}")
            conn.rollback()
            continue
    
    cur.close()
    conn.close()
    
    return stats

def main():
    # Environment check
    if not API_KEY:
        print("❌ ERROR: ODDS_API_KEY not found in .env file")
        print(f"Looking for .env file at: {os.path.join(os.path.dirname(__file__), '.env')}")
        return
    
    if not DB_PASSWORD:
        print("❌ ERROR: DB_PASSWORD not found in .env file")
        return
    
    # Test API connection first
    if not test_api_connection():
        print("❌ API connection test failed. Stopping execution.")
        return
    
    # Test database connection
    if not test_database_connection():
        print("❌ Database connection test failed. Stopping execution.")
        return
    
    print(f"\n🚀 Starting odds collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Database initialization
    try:
        init_database()
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print("Make sure PostgreSQL is running and credentials are correct in .env")
        return
    
    all_data = []
    league_stats = {}
    
    # Fetch data for each league
    for i, (league_name, sport_key) in enumerate(LEAGUES.items(), 1):
        print(f"\n📊 Processing league {i}/{len(LEAGUES)}: {league_name}")
        games = fetch_league_odds(league_name, sport_key)
        all_data.extend(games)
        league_stats[league_name] = len(games)
        
        # Add delay between leagues
        if i < len(LEAGUES):
            print(f"⏳ Waiting 10 seconds before next league...")
            time.sleep(10)
    
    if not all_data:
        print("\n❌ No data collected. Possible causes:")
        print("   - API key issues")
        print("   - Rate limiting")
        print("   - Network connectivity")
        print("   - No matches available for selected leagues")
        print("💡 Try running the script again in a few minutes.")
        return
    
    # Display collection summary
    print(f"\n{'='*60}")
    print("📈 COLLECTION SUMMARY")
    print(f"{'='*60}")
    for league, count in league_stats.items():
        print(f"{league}: {count} matches")
    print(f"Total matches: {sum(league_stats.values())}")
    
    # Save to database
    print(f"\n{'='*60}")
    print("💾 SAVING TO DATABASE")
    print(f"{'='*60}")
    
    stats = save_to_database(all_data)
    
    print(f"✅ Matches saved: {stats['matches']}")
    print(f"✅ Odds records saved: {stats['odds_records']}")
    print(f"\n🎉 Data saved to PostgreSQL database: {DB_NAME}")
    print(f"🔗 Check your API usage at: https://the-odds-api.com/account/")

if __name__ == "__main__":
    main()