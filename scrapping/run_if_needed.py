import os
import psycopg2
import subprocess
import sys

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "betting_odds")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def should_run_scraper():
    conn = None
    try:
        print("Checking database to see if scrapers need to run...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        # Check if matches table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'matches'
            );
        """)
        exists = cur.fetchone()[0]
        
        if not exists:
            print("Database tables not found. Scraper needs to run.")
            return True
            
        # Clean up matches older than today to keep the DB fresh
        cur.execute("DELETE FROM odds WHERE match_id IN (SELECT id FROM matches WHERE kickoff < CURRENT_DATE);")
        cur.execute("DELETE FROM matches WHERE kickoff < CURRENT_DATE;")
        deleted_count = cur.rowcount
        conn.commit()
        
        if deleted_count > 0:
            print(f"Deleted {deleted_count} old matches from the past.")
        
        # Check if we have upcoming matches
        cur.execute("SELECT COUNT(*) FROM matches WHERE kickoff >= CURRENT_DATE;")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("No upcoming matches found in the database. Scraper needs to run.")
            return True
            
        print(f"Database is up to date. Found {count} upcoming matches. Skipping scraper.")
        return False
        
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}. Assuming first run.")
        return True
    except Exception as e:
        print(f"Error checking database: {e}. Defaulting to running scrapers.")
        return True
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if should_run_scraper():
        print("\n--- Running Odds Scraper ---")
        subprocess.run(["uv", "run", "python", "scrapping/odds_scraper.py"])
        
        print("\n--- Running RAG Context Updater ---")
        subprocess.run(["uv", "run", "python", "scrapping/update_context.py"])
        
        print("\n--- Scraping Pipeline Complete ---")
    else:
        print("Skipping scraping pipeline to save API calls and execution time.")
