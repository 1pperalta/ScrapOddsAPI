import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class LiveOddsService:
    """Service to connect Gemini agent to live PostgreSQL odds database"""
    
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "betting_odds"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD")
        )
    
    def get_upcoming_matches_for_team(self, team_name, limit=5):
        """Get upcoming matches with odds for a specific team"""
        cur = self.conn.cursor()
        
        query = """
        SELECT DISTINCT
            m.id,
            l.name as league,
            t1.name as home_team,
            t2.name as away_team,
            m.kickoff
        FROM matches m
        JOIN leagues l ON m.league_id = l.id
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        WHERE m.kickoff > NOW()
        AND (t1.name ILIKE %s OR t2.name ILIKE %s)
        ORDER BY m.kickoff ASC
        LIMIT %s
        """
        
        cur.execute(query, (f"%{team_name}%", f"%{team_name}%", limit))
        matches = cur.fetchall()
        cur.close()
        
        # Get odds for each match
        result = []
        for match in matches:
            match_id = match[0]
            odds_data = self._get_odds_for_match(match_id)
            
            result.append({
                "match_id": match_id,
                "league": match[1],
                "home_team": match[2],
                "away_team": match[3],
                "kickoff": match[4].strftime("%Y-%m-%d %H:%M"),
                "odds": odds_data
            })
        
        return result
    
    def _get_odds_for_match(self, match_id):
        """Get all odds for a specific match"""
        cur = self.conn.cursor()
        
        query = """
        SELECT 
            b.name as bookmaker,
            o.outcome,
            o.price,
            b.region
        FROM odds o
        JOIN bookmakers b ON o.bookmaker_id = b.id
        WHERE o.match_id = %s
        ORDER BY b.name, o.outcome
        """
        
        cur.execute(query, (match_id,))
        odds = cur.fetchall()
        cur.close()
        
        # Group by outcome to find best odds
        grouped = {}
        for bookmaker, outcome, price, region in odds:
            if outcome not in grouped:
                grouped[outcome] = []
            grouped[outcome].append({
                "bookmaker": bookmaker,
                "price": float(price),
                "region": region
            })
        
        # Find best odds for each outcome
        best_odds = {}
        for outcome, odds_list in grouped.items():
            best = max(odds_list, key=lambda x: x['price'])
            best_odds[outcome] = {
                "best_price": best['price'],
                "best_bookmaker": best['bookmaker'],
                "all_bookmakers": odds_list
            }
        
        return best_odds
    
    def get_match_analysis_data(self, home_team, away_team):
        """Get complete data for a specific match analysis"""
        cur = self.conn.cursor()
        
        query = """
        SELECT 
            m.id,
            l.name as league,
            m.kickoff
        FROM matches m
        JOIN leagues l ON m.league_id = l.id
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        WHERE t1.name ILIKE %s AND t2.name ILIKE %s
        AND m.kickoff > NOW()
        ORDER BY m.kickoff ASC
        LIMIT 1
        """
        
        cur.execute(query, (f"%{home_team}%", f"%{away_team}%"))
        match = cur.fetchone()
        cur.close()
        
        if not match:
            return None
        
        match_id = match[0]
        odds_data = self._get_odds_for_match(match_id)
        
        return {
            "match_id": match_id,
            "league": match[1],
            "home_team": home_team,
            "away_team": away_team,
            "kickoff": match[2].strftime("%Y-%m-%d %H:%M"),
            "odds": odds_data
        }
    
    def get_all_upcoming_matches(self, league=None, limit=20):
        """Get all upcoming matches with odds"""
        cur = self.conn.cursor()
        
        query = """
        SELECT DISTINCT
            m.id,
            l.name as league,
            t1.name as home_team,
            t2.name as away_team,
            m.kickoff
        FROM matches m
        JOIN leagues l ON m.league_id = l.id
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        WHERE m.kickoff > NOW()
        """
        
        params = []
        if league:
            query += " AND l.name ILIKE %s"
            params.append(f"%{league}%")
        
        query += " ORDER BY m.kickoff ASC LIMIT %s"
        params.append(limit)
        
        cur.execute(query, params)
        matches = cur.fetchall()
        cur.close()
        
        result = []
        for match in matches:
            result.append({
                "match_id": match[0],
                "league": match[1],
                "home_team": match[2],
                "away_team": match[3],
                "kickoff": match[4].strftime("%Y-%m-%d %H:%M")
            })
        
        return result
    
    def close(self):
        if self.conn:
            self.conn.close()