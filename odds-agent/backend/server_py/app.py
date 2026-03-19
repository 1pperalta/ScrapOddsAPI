from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from server_py.graph import invoke_agent
from server_py.budget import get_budget_tracker
from server_py.services.odds_service import LiveOddsService
from server_py.services.rag_service import get_rag_service

app = Flask(__name__)
CORS(app)


@app.route('/api/agent/analyze-team', methods=['POST'])
def analyze_team():
    try:
        data = request.get_json()
        team = data.get('team', '').strip()
        query = data.get('query', '')

        prompt = query if query else f"Analyze the team {team} with upcoming odds and context"
        if team and team.lower() not in prompt.lower():
            prompt = f"{prompt} (team: {team})"

        analysis = invoke_agent(prompt)
        return jsonify({'analysis': analysis, 'team': team})
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

        prompt = query if query else f"Analyze the match {home_team} vs {away_team}"
        if home_team and home_team.lower() not in prompt.lower():
            prompt = f"{prompt} ({home_team} vs {away_team})"

        analysis = invoke_agent(prompt)
        return jsonify({
            'analysis': analysis,
            'home_team': home_team,
            'away_team': away_team,
        })
    except Exception as e:
        print(f"Error in analyze_match: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/value-bets', methods=['POST'])
def value_bets():
    try:
        data = request.get_json()
        league = data.get('league', '')
        query = data.get('query', '')

        prompt = query if query else f"Find the best value bets in {league}"
        if league and league.lower() not in prompt.lower():
            prompt = f"{prompt} (league: {league})"

        analysis = invoke_agent(prompt)
        return jsonify({'analysis': analysis, 'league': league})
    except Exception as e:
        print(f"Error in value_bets: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/process', methods=['POST'])
def process_general():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'analysis': 'Please provide a query.', 'query_type': 'empty'})

        analysis = invoke_agent(query)
        return jsonify({'analysis': analysis, 'query_type': 'agent'})
    except Exception as e:
        print(f"Error in process_general: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/direct-search', methods=['POST'])
def direct_search():
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')

        service = LiveOddsService()
        try:
            match_data = service.get_match_analysis_data(home_team, away_team)
            if not match_data:
                match_data = service.get_match_analysis_data(away_team, home_team)
        finally:
            service.close()

        if not match_data:
            return jsonify({
                'found': False,
                'message': f'No upcoming match found between {home_team} and {away_team}.'
            }), 404

        structured = {
            "match_info": {
                "home_team": match_data['home_team'],
                "away_team": match_data['away_team'],
                "league": match_data['league'],
                "kickoff": match_data['kickoff'],
            },
            "odds": {}
        }
        for outcome, data_item in match_data['odds'].items():
            structured["odds"][outcome] = {
                "best_price": data_item['best_price'],
                "best_bookmaker": data_item['best_bookmaker'],
                "all_bookmakers": data_item['all_bookmakers'],
                "average_price": sum(bm['price'] for bm in data_item['all_bookmakers']) / len(data_item['all_bookmakers']),
            }

        return jsonify({'found': True, 'match_data': structured})
    except Exception as e:
        print(f"Error in direct_search: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quick-matches', methods=['GET'])
def quick_matches():
    try:
        service = LiveOddsService()
        matches = service.get_all_upcoming_matches(league=None, limit=20)
        service.close()

        matches_with_odds = [m for m in matches if m.get('odds')]
        random.shuffle(matches_with_odds)

        quick_options = [
            f"{m['home_team']} vs {m['away_team']}"
            for m in matches_with_odds[:4]
        ]
        return jsonify({'matches': quick_options})
    except Exception:
        print(f"Error in quick_matches: {traceback.format_exc()}")
        return jsonify({'matches': [
            "Arsenal vs Chelsea",
            "Manchester United vs Liverpool",
            "Manchester City vs Tottenham",
            "Newcastle vs Brighton",
        ]})


@app.route('/api/rag/status', methods=['GET'])
def rag_status():
    try:
        rag_service = get_rag_service()
        info = rag_service.get_collection_info()
        return jsonify({'status': 'success', 'rag': info})
    except Exception as e:
        print(f"Error in rag_status: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'RAG system may not be initialized. Run embedding_manager.py first.',
        }), 500


@app.route('/api/rag/teams', methods=['GET'])
def rag_teams():
    try:
        rag_service = get_rag_service()
        if not rag_service.collection:
            return jsonify({'status': 'error', 'message': 'RAG collection not initialized'}), 500

        results = rag_service.collection.get(include=["metadatas"])
        teams = []
        if results['ids']:
            for metadata in results['metadatas']:
                teams.append({
                    'team': metadata.get('team', 'Unknown'),
                    'league': metadata.get('league', 'Unknown'),
                    'position': metadata.get('position', 0),
                    'updated': metadata.get('updated', 'Unknown'),
                })
        teams.sort(key=lambda x: (x['league'], x['position']))
        return jsonify({'status': 'success', 'total_teams': len(teams), 'teams': teams})
    except Exception as e:
        print(f"Error in rag_teams: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/budget', methods=['GET'])
def budget_status():
    tracker = get_budget_tracker()
    return jsonify(tracker.get_status())


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'agent': 'langgraph-deepseek-v3.1',
        'rag': 'enabled',
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3001))
    print(f"Starting Flask server on port {port}...")
    print(f"Server: http://localhost:{port}")
    print(f"Health: http://localhost:{port}/api/health")
    print(f"Budget: http://localhost:{port}/api/budget")
    app.run(debug=True, host='0.0.0.0', port=port)
