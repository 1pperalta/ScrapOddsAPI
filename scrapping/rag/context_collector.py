"""
Context Data Collector

Fetches team context data from Football-Data.org API.
Collects standings, fixtures, and statistics for all tracked leagues.
"""

import httpx
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from .config import (
    FOOTBALL_DATA_API_KEY,
    FOOTBALL_DATA_BASE_URL,
    LEAGUES,
    LEAGUES_PATH,
    DATA_PATH,
    API_RATE_LIMIT_DELAY,
    MAX_RECENT_MATCHES,
    CURRENT_SEASON
)


class ContextCollector:
    """Collects team context data from Football-Data.org API"""
    
    def __init__(self):
        self.api_key = FOOTBALL_DATA_API_KEY
        self.base_url = FOOTBALL_DATA_BASE_URL
        self.headers = {"X-Auth-Token": self.api_key}
        
        if not self.api_key:
            raise ValueError("FOOTBALL_DATA_API_KEY not found in environment variables")
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make HTTP request to Football-Data.org API with rate limiting"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error fetching {endpoint}: {e}")
            return None
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None
    
    def collect_league_standings(self, league_id: int) -> Optional[Dict]:
        """Fetch current standings for a league"""
        print(f"  Fetching standings for league {league_id}...")
        data = self._make_request(f"competitions/{league_id}/standings")
        time.sleep(API_RATE_LIMIT_DELAY)
        return data
    
    def collect_league_matches(self, league_id: int) -> Optional[Dict]:
        """Fetch recent and upcoming matches for a league"""
        print(f"  Fetching matches for league {league_id}...")
        
        # Get matches from last 30 days and next 30 days
        date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        data = self._make_request(
            f"competitions/{league_id}/matches?dateFrom={date_from}&dateTo={date_to}"
        )
        time.sleep(API_RATE_LIMIT_DELAY)
        return data
    
    def _extract_team_form(self, team_name: str, matches: List[Dict]) -> str:
        """Extract last 5 match results for a team (W/D/L format)"""
        team_matches = []
        
        for match in matches:
            if match['status'] != 'FINISHED':
                continue
            
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            
            if team_name not in [home_team, away_team]:
                continue
            
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
            
            if home_score is None or away_score is None:
                continue
            
            # Determine result from team's perspective
            if team_name == home_team:
                if home_score > away_score:
                    result = 'W'
                elif home_score < away_score:
                    result = 'L'
                else:
                    result = 'D'
            else:
                if away_score > home_score:
                    result = 'W'
                elif away_score < home_score:
                    result = 'L'
                else:
                    result = 'D'
            
            team_matches.append({
                'result': result,
                'date': match['utcDate']
            })
        
        # Sort by date descending and take last 5
        team_matches.sort(key=lambda x: x['date'], reverse=True)
        form = ''.join([m['result'] for m in team_matches[:MAX_RECENT_MATCHES]])
        
        return form if form else 'N/A'
    
    def _extract_recent_matches(self, team_name: str, matches: List[Dict]) -> List[Dict]:
        """Extract recent match details for a team"""
        team_matches = []
        
        for match in matches:
            if match['status'] != 'FINISHED':
                continue
            
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            
            if team_name not in [home_team, away_team]:
                continue
            
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
            
            if home_score is None or away_score is None:
                continue
            
            is_home = team_name == home_team
            opponent = away_team if is_home else home_team
            
            if is_home:
                if home_score > away_score:
                    result = 'W'
                elif home_score < away_score:
                    result = 'L'
                else:
                    result = 'D'
            else:
                if away_score > home_score:
                    result = 'W'
                elif away_score < home_score:
                    result = 'L'
                else:
                    result = 'D'
            
            team_matches.append({
                'date': match['utcDate'][:10],
                'opponent': opponent,
                'result': result,
                'score': f"{home_score}-{away_score}",
                'home_away': 'home' if is_home else 'away'
            })
        
        # Sort by date descending and take last 5
        team_matches.sort(key=lambda x: x['date'], reverse=True)
        return team_matches[:MAX_RECENT_MATCHES]
    
    def collect_league_data(self, league_name: str, league_info: Dict) -> Dict:
        """Collect complete data for a league"""
        print(f"\nCollecting data for {league_name}...")
        
        league_id = league_info['id']
        
        # Fetch standings
        standings_data = self.collect_league_standings(league_id)
        if not standings_data:
            print(f"  Failed to fetch standings for {league_name}")
            return None
        
        # Fetch matches
        matches_data = self.collect_league_matches(league_id)
        if not matches_data:
            print(f"  Failed to fetch matches for {league_name}")
            matches = []
        else:
            matches = matches_data.get('matches', [])
        
        # Extract standings
        standings = standings_data.get('standings', [])
        if not standings:
            print(f"  No standings found for {league_name}")
            return None
        
        # Get the main standings table (index 0 is usually the overall table)
        table = standings[0].get('table', [])
        
        # Build league data structure
        league_data = {
            "league": league_name,
            "league_id": league_id,
            "league_code": league_info['code'],
            "country": league_info['country'],
            "season": CURRENT_SEASON,
            "last_updated": datetime.now().isoformat(),
            "teams": {}
        }
        
        # Process each team
        for standing in table:
            team = standing['team']
            team_name = team['name']
            
            league_data['teams'][team_name] = {
                "team_id": team['id'],
                "position": standing['position'],
                "played": standing['playedGames'],
                "won": standing['won'],
                "drawn": standing['draw'],
                "lost": standing['lost'],
                "points": standing['points'],
                "goals_for": standing['goalsFor'],
                "goals_against": standing['goalsAgainst'],
                "goal_difference": standing['goalDifference'],
                "form": self._extract_team_form(team_name, matches),
                "recent_matches": self._extract_recent_matches(team_name, matches),
                "home_record": {
                    "played": standing.get('home', {}).get('played', 0),
                    "won": standing.get('home', {}).get('won', 0),
                    "drawn": standing.get('home', {}).get('draw', 0),
                    "lost": standing.get('home', {}).get('lost', 0)
                },
                "away_record": {
                    "played": standing.get('away', {}).get('played', 0),
                    "won": standing.get('away', {}).get('won', 0),
                    "drawn": standing.get('away', {}).get('draw', 0),
                    "lost": standing.get('away', {}).get('lost', 0)
                }
            }
        
        print(f"  Collected data for {len(league_data['teams'])} teams")
        return league_data
    
    def save_league_data(self, league_name: str, league_data: Dict):
        """Save league data to JSON file"""
        filename = LEAGUES_PATH / f"{league_name.lower().replace(' ', '_')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(league_data, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved to {filename}")
    
    def collect_all_leagues(self):
        """Collect data for all configured leagues"""
        print("Starting data collection for all leagues...")
        print(f"Data will be saved to: {LEAGUES_PATH}")
        
        collected_count = 0
        failed_leagues = []
        
        for league_name, league_info in LEAGUES.items():
            try:
                league_data = self.collect_league_data(league_name, league_info)
                
                if league_data:
                    self.save_league_data(league_name, league_data)
                    collected_count += 1
                else:
                    failed_leagues.append(league_name)
            except Exception as e:
                print(f"  Error collecting {league_name}: {e}")
                failed_leagues.append(league_name)
        
        # Save metadata
        meta = {
            "last_updated": datetime.now().isoformat(),
            "leagues_collected": collected_count,
            "leagues_failed": failed_leagues,
            "total_leagues": len(LEAGUES)
        }
        
        meta_path = DATA_PATH / "meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
        
        print(f"\nCollection complete!")
        print(f"  Success: {collected_count}/{len(LEAGUES)} leagues")
        if failed_leagues:
            print(f"  Failed: {', '.join(failed_leagues)}")


def main():
    """Main execution function"""
    collector = ContextCollector()
    collector.collect_all_leagues()


if __name__ == "__main__":
    main()

