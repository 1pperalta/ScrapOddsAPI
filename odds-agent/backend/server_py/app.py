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
        team = data.get('team')
        
        if not team:
            return jsonify({'error': 'Team name is required'}), 400
        
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
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        if not home_team or not away_team:
            return jsonify({'error': 'Both home_team and away_team are required'}), 400
        
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
        min_value_threshold = data.get('min_value_threshold', 1.05)
        
        print(f"🔍 Finding value bets for league: {league}")
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
        
        # Specific match analysis
        if 'vs' in query_lower or 'against' in query_lower:
            teams = re.split(r'\s+vs\s+|\s+against\s+', query, flags=re.IGNORECASE)
            if len(teams) == 2:
                analysis_result = analyze_specific_match(teams[0].strip(), teams[1].strip())
                return jsonify({'analysis': analysis_result, 'query_type': 'match_analysis'})
        
        # Value bets queries
        elif any(keyword in query_lower for keyword in [
            'value bet', 'best bet', 'best odds', 'opportunities', 'mejores cuotas', 'value',
            'oportunidades', 'mejor apuesta', 'mejores apuestas'
        ]):
            analysis = get_best_value_bets(league=None, min_value_threshold=1.02)
            return jsonify({'analysis': analysis, 'query_type': 'value_bets'})
        
        # Team analysis
        elif any(keyword in query_lower for keyword in ['analiza', 'analyze', 'equipo', 'team', 'analisis']):
            # Extract team name
            words = query.split()
            team_words = [word for word in words if len(word) > 3 and word.lower() not in [
                'analiza', 'analyze', 'equipo', 'team', 'el', 'la', 'los', 'las', 
                'analisis', 'analysis', 'del', 'de', 'al'
            ]]
            if team_words:
                team_name = ' '.join(team_words[:2])
                analysis = analyze_team_with_live_odds(team_name)
                return jsonify({'analysis': analysis, 'query_type': 'team_analysis'})
        
        # General soccer/betting analysis (use analyze_general_query for remaining queries)
        analysis = analyze_general_query(query)
        return jsonify({'analysis': analysis, 'query_type': 'general_sports'})
        
    except Exception as e:
        print(f"Error in process_general: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/direct-search', methods=['POST'])
def direct_search():
    """Direct search endpoint for match data with all bookmakers"""
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        print(f"🔍 DIRECT SEARCH: {home_team} vs {away_team}")
        
        # Get structured match data
        match_data = get_direct_match_data(home_team, away_team)
        
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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'agent': 'gemini',
        'functions': ['analyze_team', 'analyze_match', 'value_bets', 'process_general']
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

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"🔧 Python path includes: {sys.path}")
    print("🌐 Server will be available at: http://localhost:3001")
    print("🏥 Health check: http://localhost:3001/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=3001)  # Changed to port 3001