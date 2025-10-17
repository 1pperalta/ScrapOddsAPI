import sys
import json
import re
from agent import analyze_team_with_live_odds, analyze_specific_match, get_best_value_bets

def extract_metadata(analysis_text):
    """Extract structured metadata from Gemini's response"""
    metadata = {}
    
    # Count matches mentioned
    matches = re.findall(r'PARTIDO \d+:', analysis_text)
    metadata['matches_analyzed'] = len(matches)
    
    # Extract bookmakers mentioned
    bookmakers = re.findall(r'\(([A-Za-z0-9\s]+)\)', analysis_text)
    unique_bookmakers = list(set(bookmakers))[:10]  # Top 10 unique
    metadata['bookmakers'] = unique_bookmakers
    
    # Count value opportunities
    value_opportunities = re.findall(r'Valor: \+(\d+\.?\d*)%', analysis_text)
    metadata['value_opportunities'] = len(value_opportunities)
    
    # Extract value percentages
    if value_opportunities:
        metadata['max_value_percentage'] = max(float(v) for v in value_opportunities)
        metadata['avg_value_percentage'] = sum(float(v) for v in value_opportunities) / len(value_opportunities)
    
    # Extract top recommendations (numbered lists)
    recommendations = re.findall(r'\d+\.\s+\*\*(.*?)\*\*', analysis_text)
    if recommendations:
        metadata['top_recommendations'] = recommendations[:3]
    
    # Count warnings
    warnings = re.findall(r'⚠️|ADVERTENCIA|Advertencia', analysis_text)
    metadata['warnings_count'] = len(warnings)
    
    return metadata

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "analyze_team":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Team name required"}))
                sys.exit(1)
            
            team = sys.argv[2]
            result = analyze_team_with_live_odds(team)
            metadata = extract_metadata(result)
            
            print(json.dumps({
                "analysis": result,
                "metadata": metadata,
                "team": team
            }, ensure_ascii=False))
        
        elif command == "analyze_match":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "Home and away team names required"}))
                sys.exit(1)
            
            home_team = sys.argv[2]
            away_team = sys.argv[3]
            result = analyze_specific_match(home_team, away_team)
            metadata = extract_metadata(result)
            
            print(json.dumps({
                "analysis": result,
                "metadata": metadata,
                "home_team": home_team,
                "away_team": away_team
            }, ensure_ascii=False))
        
        elif command == "value_bets":
            league = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_best_value_bets(league=league)
            metadata = extract_metadata(result)
            
            print(json.dumps({
                "analysis": result,
                "metadata": metadata,
                "league": league or "all"
            }, ensure_ascii=False))
        
        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()