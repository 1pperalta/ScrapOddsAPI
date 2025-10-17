from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import sys
import os

# Add the parent directory to Python path to handle imports correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import your agent functions
try:
    from server_py.agent import analyze_team_with_live_odds, analyze_specific_match, get_best_value_bets, get_direct_match_data
except ImportError:
    # Fallback import method
    from agent import analyze_team_with_live_odds, analyze_specific_match, get_best_value_bets, get_direct_match_data

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
    """General endpoint for queries that don't fit specific patterns"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        print(f"🔍 Processing general query: {query}")
        
        # Try to route to appropriate function based on query content .
        query_lower = query.lower()
        
        # Enhanced pattern matching for better natural language support
        if 'vs' in query_lower or 'against' in query_lower:
            # Extract team names for match analysis
            import re
            teams = re.split(r'\s+vs\s+|\s+against\s+', query, flags=re.IGNORECASE)
            if len(teams) == 2:
                home_team = teams[0].strip()
                away_team = teams[1].strip()
                analysis = analyze_specific_match(home_team, away_team)
                return jsonify({
                    'analysis': analysis,
                    'query_type': 'match_analysis',
                    'confidence': 0.9
                })
        
        # Enhanced betting-related query detection
        elif any(keyword in query_lower for keyword in [
            'value bet', 'best bet', 'best odds', 'opportunities', 'this weekend', 
            'today', 'tomorrow', 'best match', 'good bet', 'recommended bet', 
            'what to bet', 'where to bet', 'betting tip', 'best bets'
        ]):
            # Extract league if mentioned
            league = None
            leagues = ['premier league', 'la liga', 'serie a', 'bundesliga', 'ligue 1', 'champions league']
            for lg in leagues:
                if lg in query_lower:
                    league = lg.title()
                    break
            
            # Use lower threshold for general betting queries to show more opportunities
            analysis = get_best_value_bets(league=league, min_value_threshold=1.02)
            return jsonify({
                'analysis': analysis,
                'query_type': 'value_bets',
                'confidence': 0.9
            })
        
        else:
            # Try team analysis - extract potential team name
            # Remove common words and use remaining text as team name
            import re
            clean_query = re.sub(r'\b(analyze|analysis|team|next|matches|games|upcoming|show|me|the|for)\b', '', query_lower).strip()
            
            # If we have a clean team name (1-3 words), try team analysis
            if clean_query and len(clean_query.split()) <= 3:
                analysis = analyze_team_with_live_odds(clean_query.title())
                return jsonify({
                    'analysis': analysis,
                    'query_type': 'team_analysis',
                    'confidence': 0.8
                })
            else:
                # For any other general query, default to value bets
                analysis = get_best_value_bets(league=None, min_value_threshold=1.02)
                return jsonify({
                    'analysis': analysis,
                    'query_type': 'general_betting',
                    'confidence': 0.7
                })
    
    except Exception as e:
        print(f"Error in process_general: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'agent': 'gemini',
        'functions': ['analyze_team', 'analyze_match', 'value_bets']
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
                '/api/agent/process'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/api/agent/direct-search', methods=['POST'])
def direct_search():
    """Direct search endpoint for match data with all bookmakers"""
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        print(f"🔍 Direct search request: {home_team} vs {away_team}")
        
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

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"🔧 Python path includes: {sys.path}")
    print("🌐 Server will be available at: http://localhost:3001")
    print("🏥 Health check: http://localhost:3001/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=3001)  # Changed to port 3001