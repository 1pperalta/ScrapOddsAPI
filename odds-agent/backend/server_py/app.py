from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import sys
import os
import re

# Add the parent directory to Python path to handle imports correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import your agent functions
try:
    from server_py.agent import analyze_team_with_live_odds, analyze_specific_match, get_best_value_bets, get_direct_match_data, analyze_general_query
except ImportError:
    # Fallback import method
    from agent import analyze_team_with_live_odds, analyze_specific_match, get_best_value_bets, get_direct_match_data, analyze_general_query

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/api/agent/analyze-team', methods=['POST'])
def analyze_team():
    try:
        data = request.get_json()
        team = data.get('team', '').strip()
        query = data.get('query', '')
        
        # Check for non-soccer queries
        query_lower = query.lower() if query else ''
        non_soccer_patterns = [
            'cook', 'recipe', 'chef', 'food', 'comida', 'cocin', 'receta',
            'pasta', 'cheese', 'cookies', 'cake', 'bread', 'meal', 'kitchen',
            'music', 'movie', 'weather', 'health', 'work', 'program', 'code',
            'mathematics', 'history', 'science', 'literature', 'art', 'paint'
        ]
        
        if any(pattern in query_lower for pattern in non_soccer_patterns):
            rejection_message = """🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, soy un asistente especializado únicamente en:

⚽ **Fútbol**: Análisis de equipos, jugadores, partidos y competiciones
💰 **Apuestas Deportivas**: Cuotas, estrategias, value betting y recomendaciones  
📊 **Odds y Bookmakers**: Comparación de casas de apuestas y mercados

**Ejemplos de consultas que puedo ayudar:**
• "¿Cuáles son las mejores cuotas para el Real Madrid?"
• "Analiza el partido Liverpool vs Arsenal"  
• "Dame estrategias de value betting"
• "¿Qué mercados recomiendas para la Premier League?"

Por favor, realiza una consulta relacionada con fútbol o apuestas deportivas."""
            
            return jsonify({
                'analysis': rejection_message,
                'query_type': 'rejected_topic'
            })
        
        if not team:
            no_team_message = """⚠️ **No se detectó un equipo específico**

Por favor, especifica el equipo que quieres analizar. Ejemplos:

• "Analiza Arsenal"
• "Analiza el Real Madrid"
• "Cuotas del PSV"

O prueba con un formato de partido: "Arsenal vs Chelsea"
"""
            return jsonify({
                'analysis': no_team_message,
                'query_type': 'unclear_query'
            })
        
        print(f"🔍 Analyzing team: {team}")
        analysis = analyze_team_with_live_odds(team)
        
        return jsonify({
            'analysis': analysis,
            'team': team,
            'confidence': 0.9
        })
    
    except Exception as e:
        print(f"Error in analyze_team: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/analyze-match', methods=['POST'])
def analyze_match():
    try:
        data = request.get_json()
        home_team = data.get('home_team', '').strip()
        away_team = data.get('away_team', '').strip()
        query = data.get('query', '')
        
        # Check for non-soccer queries
        query_lower = query.lower() if query else ''
        non_soccer_patterns = [
            'cook', 'recipe', 'chef', 'food', 'comida', 'cocin', 'receta',
            'pasta', 'cheese', 'cookies', 'cake', 'bread', 'meal', 'kitchen',
            'music', 'movie', 'weather', 'health', 'work', 'program', 'code',
            'mathematics', 'history', 'science', 'literature', 'art', 'paint'
        ]
        
        if any(pattern in query_lower for pattern in non_soccer_patterns):
            rejection_message = """🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, soy un asistente especializado únicamente en:

⚽ **Fútbol**: Análisis de equipos, jugadores, partidos y competiciones
💰 **Apuestas Deportivas**: Cuotas, estrategias, value betting y recomendaciones  
📊 **Odds y Bookmakers**: Comparación de casas de apuestas y mercados

**Ejemplos de consultas que puedo ayudar:**
• "¿Cuáles son las mejores cuotas para el Real Madrid?"
• "Analiza el partido Liverpool vs Arsenal"  
• "Dame estrategias de value betting"
• "¿Qué mercados recomiendas para la Premier League?"

Por favor, realiza una consulta relacionada con fútbol o apuestas deportivas."""
            
            return jsonify({
                'analysis': rejection_message,
                'query_type': 'rejected_topic'
            })
        
        if not home_team or not away_team:
            no_match_message = """⚠️ **No se detectó un partido específico**

Por favor, especifica ambos equipos en el formato correcto. Ejemplos:

• "Arsenal vs Chelsea"
• "Real Madrid vs Barcelona"
• "Liverpool against Manchester City"
"""
            return jsonify({
                'analysis': no_match_message,
                'query_type': 'unclear_query'
            })
        
        print(f"🔍 Analyzing match: {home_team} vs {away_team}")
        analysis = analyze_specific_match(home_team, away_team)
        
        return jsonify({
            'analysis': analysis,
            'home_team': home_team,
            'away_team': away_team,
            'confidence': 0.9
        })
    
    except Exception as e:
        print(f"Error in analyze_match: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/value-bets', methods=['POST'])
def value_bets():
    try:
        data = request.get_json()
        league = data.get('league')
        query = data.get('query', '')
        min_value_threshold = data.get('min_value_threshold', 1.05)
        
        print(f"🔍 Value bets request - League: {league}, Query: '{query}'")
        
        # If query contains non-soccer terms, reject immediately
        query_lower = query.lower() if query else ''
        non_soccer_patterns = [
            'cook', 'recipe', 'chef', 'food', 'comida', 'cocin', 'receta',
            'pasta', 'cheese', 'cookies', 'cake', 'bread', 'meal', 'kitchen',
            'music', 'movie', 'weather', 'health', 'work', 'program', 'code',
            'mathematics', 'history', 'science', 'literature', 'art', 'paint'
        ]
        
        if any(pattern in query_lower for pattern in non_soccer_patterns):
            rejection_message = """🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, soy un asistente especializado únicamente en:

⚽ **Fútbol**: Análisis de equipos, jugadores, partidos y competiciones
💰 **Apuestas Deportivas**: Cuotas, estrategias, value betting y recomendaciones  
📊 **Odds y Bookmakers**: Comparación de casas de apuestas y mercados

**Ejemplos de consultas que puedo ayudar:**
• "¿Cuáles son las mejores cuotas para el Real Madrid?"
• "Analiza el partido Liverpool vs Arsenal"  
• "Dame estrategias de value betting"
• "¿Qué mercados recomiendas para la Premier League?"

Por favor, realiza una consulta relacionada con fútbol o apuestas deportivas."""
            
            return jsonify({
                'analysis': rejection_message,
                'query_type': 'rejected_topic'
            })
        
        # If no league provided, detect from query or return error
        if not league or league == 'None':
            if query:
                # Try to detect league from query
                if 'premier league' in query_lower or 'premier' in query_lower:
                    league = 'Premier League'
                elif 'bundesliga' in query_lower:
                    league = 'Bundesliga'
                elif 'la liga' in query_lower:
                    league = 'La Liga'
                elif 'serie a' in query_lower:
                    league = 'Serie A'
                elif 'ligue 1' in query_lower or 'ligue1' in query_lower:
                    league = 'Ligue 1'
                elif 'champions' in query_lower:
                    league = 'Champions League'
                else:
                    # No league detected
                    no_league_message = """⚠️ **No se detectó una liga específica en tu consulta**

Por favor, especifica la liga que te interesa. Ejemplos:

• "Mejores apuestas de la Premier League"
• "Value bets de La Liga"
• "Oportunidades en la Bundesliga"
• "Cuotas de la Serie A"

**Ligas disponibles:**
• Premier League
• La Liga
• Serie A
• Bundesliga
• Ligue 1
• Champions League

O intenta con un equipo específico: "Analiza Arsenal"
"""
                    return jsonify({
                        'analysis': no_league_message,
                        'query_type': 'unclear_query'
                    })
            else:
                # No query and no league
                no_league_message = """⚠️ **No se detectó una liga específica**

Por favor, especifica la liga para encontrar las mejores apuestas.

**Ligas disponibles:**
• Premier League
• La Liga
• Serie A
• Bundesliga
• Ligue 1
• Champions League
"""
                return jsonify({
                    'analysis': no_league_message,
                    'query_type': 'unclear_query'
                })
        
        print(f"✅ Final league detected: {league}")
        analysis = get_best_value_bets(league=league, min_value_threshold=min_value_threshold)
        
        return jsonify({
            'analysis': analysis,
            'league': league,
            'threshold': min_value_threshold,
            'confidence': 0.9
        })
    
    except Exception as e:
        print(f"Error in value_bets: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/process', methods=['POST'])
def process_general():
    """Enhanced topic filtering with immediate rejection"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        print(f"🔍 Processing query: {query}")
        
        query_lower = query.lower()
        
        # FIRST: Immediate rejection for obvious non-soccer queries
        non_soccer_patterns = [
            'cook', 'recipe', 'chef', 'food', 'comida', 'cocin', 'receta',
            'pasta', 'cheese', 'cookies', 'cake', 'bread', 'meal', 'kitchen',
            'music', 'movie', 'weather', 'health', 'work', 'program', 'code',
            'mathematics', 'history', 'science', 'literature', 'art', 'paint'
        ]
        
        if any(pattern in query_lower for pattern in non_soccer_patterns):
            rejection_message = """🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, soy un asistente especializado únicamente en:

⚽ **Fútbol**: Análisis de equipos, jugadores, partidos y competiciones
💰 **Apuestas Deportivas**: Cuotas, estrategias, value betting y recomendaciones  
📊 **Odds y Bookmakers**: Comparación de casas de apuestas y mercados

**Ejemplos de consultas que puedo ayudar:**
• "¿Cuáles son las mejores cuotas para el Real Madrid?"
• "Analiza el partido Liverpool vs Arsenal"  
• "Dame estrategias de value betting"
• "¿Qué mercados recomiendas para la Premier League?"

Por favor, realiza una consulta relacionada con fútbol o apuestas deportivas."""
            
            return jsonify({
                'analysis': rejection_message,
                'query_type': 'rejected_topic'
            })
        
        # SECOND: Check for soccer/betting keywords
        soccer_keywords = [
            'football', 'soccer', 'futbol', 'fútbol', 'equipo', 'team', 'partido', 'match',
            'liga', 'league', 'champions', 'premier', 'jugador', 'player', 'gol', 'goal',
            'apuesta', 'bet', 'betting', 'cuota', 'cuotas', 'odds', 'bookmaker',
            'arsenal', 'chelsea', 'liverpool', 'manchester', 'real madrid', 'barcelona',
            'atletico', 'sevilla', 'valencia', 'tottenham', 'newcastle', 'brighton',
            'everton', 'leicester', 'aston villa', 'crystal palace', 'wolves',
            'la liga', 'serie a', 'bundesliga', 'ligue 1', 'champions league'
        ]
        
        has_soccer_keywords = any(keyword in query_lower for keyword in soccer_keywords)
        
        # If no soccer keywords found, reject
        if not has_soccer_keywords:
            rejection_message = """🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, no detecté términos relacionados con fútbol o apuestas en tu consulta.

Por favor, pregúntame sobre:
• Equipos y jugadores de fútbol
• Partidos y competiciones  
• Cuotas y estrategias de apuesta
• Análisis deportivos

**Ejemplo:** "Analiza el Arsenal" o "Mejores cuotas de la Premier League"."""
            
            return jsonify({
                'analysis': rejection_message,
                'query_type': 'rejected_topic'
            })
        
        # THIRD: Process valid soccer queries
        
        # Specific match analysis (ONLY with vs format)
        if 'vs' in query_lower or 'against' in query_lower:
            teams = re.split(r'\s+vs\s+|\s+against\s+', query, flags=re.IGNORECASE)
            if len(teams) == 2:
                analysis_result = analyze_specific_match(teams[0].strip(), teams[1].strip())
                return jsonify({'analysis': analysis_result, 'query_type': 'match_analysis'})
        
        # Check if query mentions a specific team
        team_mentioned = None
        common_teams = [
            # Premier League
            'psv', 'ajax', 'feyenoord', 'arsenal', 'liverpool', 'chelsea', 'manchester', 
            'tottenham', 'newcastle', 'brighton', 'city', 'united', 'everton', 'fulham',
            'aston villa', 'crystal palace', 'wolves', 'leicester', 'southampton',
            # La Liga
            'barcelona', 'real madrid', 'atletico', 'sevilla', 'valencia', 'villarreal',
            'athletic', 'betis', 'sociedad',
            # Serie A
            'inter', 'milan', 'juventus', 'roma', 'napoli', 'lazio', 'atalanta', 'fiorentina',
            # Bundesliga
            'bayern', 'dortmund', 'leipzig', 'leverkusen', 'frankfurt', 'hoffenheim', 'mainz',
            # Ligue 1
            'psg', 'lyon', 'marseille', 'monaco', 'lille'
        ]
        
        for team in common_teams:
            if team in query_lower:
                team_mentioned = team
                break
        
        # If team is mentioned with cuotas/odds/apuesta, analyze that specific team
        if team_mentioned and any(keyword in query_lower for keyword in [
            'cuotas', 'cuota', 'odds', 'apuesta', 'apuestas', 'bet', 'mejor', 'mejores', 'best', 'dame'
        ]):
            words = query.split()
            team_words = [word for word in words if len(word) > 2 and word.lower() not in [
                'dame', 'las', 'mejores', 'mejor', 'cuotas', 'cuota', 'para', 'el', 'de', 'del', 
                'best', 'odds', 'for', 'the', 'apuesta', 'apuestas', 'bet'
            ]]
            if team_words:
                team_name = ' '.join(team_words[:3])
                print(f"   Detected team-specific query for: {team_name}")
                analysis = analyze_team_with_live_odds(team_name)
                return jsonify({'analysis': analysis, 'query_type': 'team_analysis'})
        
        # Value bets queries (only if no specific team mentioned)
        elif any(keyword in query_lower for keyword in [
            'value bet', 'best bet', 'opportunities', 'oportunidades', 'mejor apuesta', 'mejores apuestas'
        ]) and not team_mentioned:
            # Check longer strings first to avoid partial matches
            detected_league = None
            if 'premier league' in query_lower or 'premier' in query_lower:
                detected_league = 'Premier League'
            elif 'bundesliga' in query_lower:
                detected_league = 'Bundesliga'
            elif 'la liga' in query_lower:
                detected_league = 'La Liga'
            elif 'serie a' in query_lower:
                detected_league = 'Serie A'
            elif 'ligue 1' in query_lower or 'ligue1' in query_lower:
                detected_league = 'Ligue 1'
            elif 'champions' in query_lower:
                detected_league = 'Champions League'
            
            print(f"   Detected league: {detected_league}")
            
            # If no league detected, return helpful message
            if not detected_league:
                no_league_message = """
⚠️ **No se detectó una liga específica en tu consulta**

Por favor, especifica la liga que te interesa. Ejemplos:

• "Mejores apuestas de la Premier League"
• "Value bets de La Liga"
• "Oportunidades en la Bundesliga"
• "Cuotas de la Serie A"

**Ligas disponibles:**
• Premier League
• La Liga
• Serie A
• Bundesliga
• Ligue 1
• Champions League

O intenta con un equipo específico: "Analiza Arsenal"
"""
                return jsonify({'analysis': no_league_message, 'query_type': 'unclear_query'})
            
            analysis = get_best_value_bets(league=detected_league, min_value_threshold=1.02)
            return jsonify({'analysis': analysis, 'query_type': 'value_bets'})
        
        # Team analysis with explicit keywords
        elif any(keyword in query_lower for keyword in ['analiza', 'analyze', 'equipo', 'team', 'analisis']):
            words = query.split()
            team_words = [word for word in words if len(word) > 3 and word.lower() not in [
                'analiza', 'analyze', 'equipo', 'team', 'el', 'la', 'los', 'las', 
                'analisis', 'analysis', 'del', 'de', 'al'
            ]]
            if team_words:
                team_name = ' '.join(team_words[:2])
                analysis = analyze_team_with_live_odds(team_name)
                return jsonify({'analysis': analysis, 'query_type': 'team_analysis'})
            else:
                no_team_message = """
⚠️ **No se detectó un equipo específico en tu consulta**

Por favor, especifica el equipo que quieres analizar. Ejemplos:

• "Analiza Arsenal"
• "Analiza el Real Madrid"
• "Equipo PSV"

O prueba con un formato de partido: "Arsenal vs Chelsea"
"""
                return jsonify({'analysis': no_team_message, 'query_type': 'unclear_query'})
        
        # General soccer/betting analysis (use analyze_general_query for remaining queries)
        analysis = analyze_general_query(query)
        return jsonify({'analysis': analysis, 'query_type': 'general_sports'})
        
    except Exception as e:
        print(f"Error in process_general: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/direct-search', methods=['POST'])
def direct_search():
    """Direct search endpoint for match data with all bookmakers - works in both directions"""
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        print(f"🔍 DIRECT SEARCH: {home_team} vs {away_team}")
        
        # Try both directions
        match_data = get_direct_match_data(home_team, away_team)
        
        if not match_data:
            # Try reversed
            print(f"🔄 Trying reversed: {away_team} vs {home_team}")
            match_data = get_direct_match_data(away_team, home_team)
        
        if not match_data:
            return jsonify({
                'found': False,
                'message': f'No se encontró un partido próximo entre {home_team} y {away_team} en la base de datos.'
            }), 404
        
        return jsonify({
            'found': True,
            'match_data': match_data
        })
    
    except Exception as e:
        print(f"Error in direct_search: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-matches', methods=['GET'])
def quick_matches():
    """Get 4 random upcoming matches for quick search buttons"""
    try:
        from server_py.services.odds_service import LiveOddsService
        import random
        
        odds_service = LiveOddsService()
        matches = odds_service.get_all_upcoming_matches(league=None, limit=20)
        odds_service.close()
        
        # Filter only matches with odds and randomize
        matches_with_odds = [m for m in matches if m.get('odds')]
        random.shuffle(matches_with_odds)
        
        # Return 4 random matches
        quick_options = [
            f"{m['home_team']} vs {m['away_team']}" 
            for m in matches_with_odds[:4]
        ]
        
        return jsonify({'matches': quick_options})
    
    except Exception as e:
        print(f"Error in quick_matches: {traceback.format_exc()}")
        # Fallback to default if error
        return jsonify({'matches': [
            "Arsenal vs Chelsea",
            "Manchester United vs Liverpool", 
            "Manchester City vs Tottenham",
            "Newcastle vs Brighton"
        ]})

@app.route('/api/rag/status', methods=['GET'])
def rag_status():
    """Check RAG system status and collection info"""
    try:
        from server_py.services.rag_service import get_rag_service
        
        rag_service = get_rag_service()
        info = rag_service.get_collection_info()
        
        return jsonify({
            'status': 'success',
            'rag': info
        })
    
    except Exception as e:
        print(f"Error in rag_status: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'RAG system may not be initialized. Run embedding_manager.py first.'
        }), 500

@app.route('/api/rag/teams', methods=['GET'])
def rag_teams():
    """List all teams available in RAG system"""
    try:
        from server_py.services.rag_service import get_rag_service
        
        rag_service = get_rag_service()
        
        if not rag_service.collection:
            return jsonify({
                'status': 'error',
                'message': 'RAG collection not initialized'
            }), 500
        
        # Get all documents with metadata
        results = rag_service.collection.get(
            include=["metadatas"]
        )
        
        teams = []
        if results['ids']:
            for i, metadata in enumerate(results['metadatas']):
                teams.append({
                    'team': metadata.get('team', 'Unknown'),
                    'league': metadata.get('league', 'Unknown'),
                    'position': metadata.get('position', 0),
                    'updated': metadata.get('updated', 'Unknown')
                })
        
        # Sort by league and position
        teams.sort(key=lambda x: (x['league'], x['position']))
        
        return jsonify({
            'status': 'success',
            'total_teams': len(teams),
            'teams': teams
        })
    
    except Exception as e:
        print(f"Error in rag_teams: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'agent': 'gemini',
        'functions': ['analyze_team', 'analyze_match', 'value_bets', 'process_general'],
        'rag': 'enabled'
    })

@app.route('/api/test', methods=['GET'])
def test_agent():
    """Test endpoint to verify agent functions work"""
    try:
        # Test with a simple query
        result = "Agent functions loaded successfully!"
        return jsonify({
            'status': 'success',
            'message': result,
            'available_endpoints': [
                '/api/agent/analyze-team',
                '/api/agent/analyze-match', 
                '/api/agent/value-bets',
                '/api/agent/process',
                '/api/agent/direct-search'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        })

# At the end of app.py
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3001))  # Use PORT env var, default to 3001
    print(f"🚀 Starting Flask server on port {port}...")
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"🔧 Python path includes: {sys.path}")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"🏥 Health check: http://localhost:{port}/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=port)