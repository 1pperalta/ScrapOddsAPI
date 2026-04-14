"""
Context Document Builder

Converts raw JSON data into rich narrative documents for RAG embedding.
Builds comprehensive text descriptions of team context, form, and statistics.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

import difflib
from .config import LEAGUES_PATH, LEAGUES, DATA_PATH


@dataclass
class Document:
    """Simple document class for storing content and metadata"""
    page_content: str
    metadata: Dict


class ContextBuilder:
    """Builds rich text documents from team JSON data"""
    
    def __init__(self):
        self.leagues_path = LEAGUES_PATH
        self.advanced_stats_path = DATA_PATH / "soccerdata" / "team_advanced_stats.json"
        self.advanced_stats = self._load_advanced_stats()
        
    def _load_advanced_stats(self) -> Dict:
        if self.advanced_stats_path.exists():
            with open(self.advanced_stats_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
        
    def _find_advanced_stats(self, league_name: str, team_name: str) -> Optional[Dict]:
        if league_name not in self.advanced_stats:
            return None
        league_stats = self.advanced_stats[league_name]
        
        # Exact match
        if team_name in league_stats:
            return league_stats[team_name]
            
        # Fuzzy match
        matches = difflib.get_close_matches(team_name, league_stats.keys(), n=1, cutoff=0.4)
        if matches:
            return league_stats[matches[0]]
            
        return None
    
    def load_league_data(self, league_name: str) -> Optional[Dict]:
        """Load league JSON data from file"""
        filename = self.leagues_path / f"{league_name.lower().replace(' ', '_')}.json"
        
        if not filename.exists():
            print(f"League file not found: {filename}")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_team_in_leagues(self, team_name: str) -> Optional[tuple]:
        """Find team data across all league files"""
        team_lower = team_name.lower()
        
        for league_name in LEAGUES.keys():
            league_data = self.load_league_data(league_name)
            
            if not league_data:
                continue
            
            # Check each team in the league
            for stored_team_name, team_data in league_data['teams'].items():
                if team_lower in stored_team_name.lower():
                    return (league_data, stored_team_name, team_data)
        
        return None
    
    def _format_form_description(self, form: str) -> str:
        """Convert form string (WWDLL) to readable description"""
        if not form or form == 'N/A':
            return "Sin datos de forma reciente"
        
        wins = form.count('W')
        draws = form.count('D')
        losses = form.count('L')
        total = len(form)
        
        desc = f"{wins} victoria{'s' if wins != 1 else ''}, "
        desc += f"{draws} empate{'s' if draws != 1 else ''}, "
        desc += f"{losses} derrota{'s' if losses != 1 else ''}"
        desc += f" en los últimos {total} partidos"
        
        return desc
    
    def _calculate_points_per_game(self, points: int, played: int) -> float:
        """Calculate average points per game"""
        if played == 0:
            return 0.0
        return round(points / played, 2)
    
    def _calculate_goals_per_game(self, goals: int, played: int) -> float:
        """Calculate average goals per game"""
        if played == 0:
            return 0.0
        return round(goals / played, 2)
    
    def build_team_document(self, team_name: str, league_name: str = None) -> Optional[Document]:
        """Build a rich text document for a team"""
        if league_name:
            # Build from specific league
            league_data = self.load_league_data(league_name)
            if not league_data:
                print(f"League not found: {league_name}")
                return None
            
            # Find team in this specific league
            actual_team_name = None
            team_data = None
            for stored_team_name, stored_team_data in league_data['teams'].items():
                if team_name.lower() in stored_team_name.lower():
                    actual_team_name = stored_team_name
                    team_data = stored_team_data
                    break
            
            if not actual_team_name:
                print(f"Team {team_name} not found in {league_name}")
                return None
        else:
            # Search across all leagues (original behavior)
            result = self.find_team_in_leagues(team_name)
            
            if not result:
                print(f"Team not found: {team_name}")
                return None
            
            league_data, actual_team_name, team_data = result
        
        # Calculate statistics
        ppg = self._calculate_points_per_game(team_data['points'], team_data['played'])
        gpg_for = self._calculate_goals_per_game(team_data['goals_for'], team_data['played'])
        gpg_against = self._calculate_goals_per_game(team_data['goals_against'], team_data['played'])
        
        # Build narrative document
        content = f"""Equipo: {actual_team_name}
Liga: {league_data['league']} ({league_data['country']})
Temporada: {league_data['season']}
Última actualización: {league_data['last_updated'][:10]}

CLASIFICACIÓN Y RENDIMIENTO:
El {actual_team_name} se encuentra en la posición {team_data['position']} de {league_data['league']} con {team_data['points']} puntos en {team_data['played']} partidos jugados.
Promedio de puntos por partido: {ppg}

RESULTADOS:
Ha logrado {team_data['won']} victorias, {team_data['drawn']} empates y {team_data['lost']} derrotas.
Forma reciente: {team_data['form']} - {self._format_form_description(team_data['form'])}

ESTADÍSTICAS OFENSIVAS Y DEFENSIVAS:
Goles a favor: {team_data['goals_for']} (promedio: {gpg_for} por partido)
Goles en contra: {team_data['goals_against']} (promedio: {gpg_against} por partido)
Diferencia de goles: {team_data['goal_difference']:+d}

RENDIMIENTO LOCAL Y VISITANTE:
Como local: {team_data['home_record']['won']} victorias, {team_data['home_record']['drawn']} empates, {team_data['home_record']['lost']} derrotas en {team_data['home_record']['played']} partidos
Como visitante: {team_data['away_record']['won']} victorias, {team_data['away_record']['drawn']} empates, {team_data['away_record']['lost']} derrotas en {team_data['away_record']['played']} partidos
"""
        
        # Add recent matches if available
        if team_data.get('recent_matches'):
            content += "\nÚLTIMOS PARTIDOS:\n"
            for match in team_data['recent_matches']:
                result_desc = {
                    'W': 'Victoria',
                    'D': 'Empate',
                    'L': 'Derrota'
                }.get(match['result'], match['result'])
                
                location = 'Local' if match['home_away'] == 'home' else 'Visitante'
                content += f"- {match['date']}: {result_desc} vs {match['opponent']} ({location}) {match['score']}\n"
                
        # Add advanced stats if available
        advanced_stats = self._find_advanced_stats(league_data['league'], actual_team_name)
        if advanced_stats:
            content += "\nESTADÍSTICAS AVANZADAS (FBref):\n"
            if 'possession_pct' in advanced_stats:
                content += f"Posesión promedio: {advanced_stats['possession_pct']}%\n"
            if 'goals_per_90' in advanced_stats:
                content += f"Goles por 90 min: {advanced_stats['goals_per_90']}\n"
            if 'shots_per_90' in advanced_stats:
                content += f"Tiros por 90 min: {advanced_stats['shots_per_90']}\n"
            if 'shots_on_target_per_90' in advanced_stats:
                content += f"Tiros al arco por 90 min: {advanced_stats['shots_on_target_per_90']}\n"
                
        # Create Document object with metadata
        document = Document(
            page_content=content,
            metadata={
                "team": actual_team_name,
                "league": league_data['league'],
                "league_code": league_data['league_code'],
                "country": league_data['country'],
                "position": team_data['position'],
                "points": team_data['points'],
                "form": team_data['form'],
                "source": "football-data.org",
                "updated": league_data['last_updated'],
                "type": "team_context"
            }
        )
        
        return document
    
    def build_all_documents(self) -> List[Document]:
        """Build documents for all teams in all leagues"""
        documents = []
        team_count = 0
        
        print("Building documents for all teams...")
        
        for league_name in LEAGUES.keys():
            league_data = self.load_league_data(league_name)
            
            if not league_data:
                print(f"  Skipping {league_name} (no data)")
                continue
            
            print(f"  Processing {league_name}...")
            
            for team_name in league_data['teams'].keys():
                # Pass league_name to ensure we build from the correct league
                doc = self.build_team_document(team_name, league_name)
                if doc:
                    documents.append(doc)
                    team_count += 1
        
        print(f"Built {team_count} team documents")
        return documents


def main():
    """Test document building"""
    builder = ContextBuilder()
    
    # Test with a single team
    test_team = "Arsenal"
    doc = builder.build_team_document(test_team)
    
    if doc:
        print(f"\nSample document for {test_team}:")
        print("=" * 60)
        print(doc.page_content[:500])
        print("...")
        print("\nMetadata:")
        print(doc.metadata)


if __name__ == "__main__":
    main()

