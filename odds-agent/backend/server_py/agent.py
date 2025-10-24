from dotenv import load_dotenv
import os
import google.generativeai as genai
from server_py.services.odds_service import LiveOddsService

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_team_with_live_odds(team: str):
    """Concise team analysis focused on betting value"""
    
    odds_service = LiveOddsService()
    matches = odds_service.get_upcoming_matches_for_team(team, limit=3)  # Reduced to 3
    odds_service.close()
    
    # Build odds context
    if matches:
        odds_context = f"🎯 **PRÓXIMOS PARTIDOS** ({len(matches)} disponibles):\n\n"
        for i, match in enumerate(matches, 1):
            odds_context += f"**{match['home_team']} vs {match['away_team']}**\n"
            odds_context += f"📅 {match['kickoff']} | 🏆 {match['league']}\n"
            for outcome, data in match['odds'].items():
                odds_context += f"• {outcome}: {data['best_price']} ({data['best_bookmaker']})\n"
            odds_context += "\n"
    else:
        odds_context = "📊 No hay cuotas disponibles para este equipo.\n\n"
    
    prompt = f"""
Eres un analista de fútbol y apuestas. Analiza {team} de forma CONCISA y DIRECTA.

{odds_context}

Responde en máximo 200 palabras con:

**Situación Actual de {team}**
Una evaluación breve de su forma reciente y posición actual.

**Análisis para Apuestas**
{"Evalúa las cuotas mostradas y recomienda" if matches else "Recomienda"} qué mercados son mejores para apostar y por qué.

**Predicción Clave**
Un pronóstico directo sobre su rendimiento próximo.

Sé específico y enfócate solo en información útil para apostar.
"""
    
    response = model.generate_content(prompt)
    return response.text

def analyze_specific_match(home_team: str, away_team: str):
    """Concise match analysis for betting"""
    
    match_data = get_direct_match_data(home_team, away_team)
    
    if match_data:
        odds_context = f"🎯 **CUOTAS DISPONIBLES**:\n\n"
        odds_context += f"📅 {match_data['kickoff']} | 🏆 {match_data['league']}\n\n"
        for outcome, data in match_data['odds'].items():
            odds_context += f"• **{outcome}**: {data['best_price']} ({data['best_bookmaker']})\n"
        odds_context += "\n"
    else:
        odds_context = "📊 No hay cuotas específicas disponibles.\n\n"
    
    prompt = f"""
Analiza {home_team} vs {away_team} de forma CONCISA para apuestas.

{odds_context}

Responde en máximo 150 palabras con:

**Factor Clave**
El aspecto más importante que decidirá el partido.

**Recomendación de Apuesta**
{"Evalúa las cuotas mostradas y sugiere" if match_data else "Sugiere"} la mejor apuesta con justificación breve.

**Predicción**
Resultado más probable y por qué.

Sé directo y enfócate solo en lo esencial para apostar.
"""
    
    response = model.generate_content(prompt)
    return {
        'analysis': response.text,
        'match_data': match_data,
        'has_odds': bool(match_data)
    }

def get_best_value_bets(league=None, min_value_threshold=1.05):
    """Concise value betting opportunities"""
    
    odds_service = LiveOddsService()
    matches = odds_service.get_all_upcoming_matches(league=league, limit=10)  # Reduced to 10
    odds_service.close()
    
    if not matches:
        prompt = f"""
Proporciona consejos CONCISOS de apuestas de valor.

Responde en máximo 100 palabras con:

**Estrategia del Momento**
Qué tipo de apuestas buscar ahora.

**Mercados Recomendados**
Los 2-3 mercados más rentables actualmente.

**Consejo Clave**
Una recomendación específica para maximizar valor.

Sé directo y práctico.
"""
    else:
        # Build concise matches context
        matches_context = "🎯 **TOP OPORTUNIDADES**:\n\n"
        for i, match in enumerate(matches[:5], 1):  # Only top 5
            matches_context += f"**{match['home_team']} vs {match['away_team']}**\n"
            matches_context += f"📅 {match['kickoff']} | "
            # Show only best odds
            if match.get('odds') and len(match['odds']) > 0:
                best_odds = max(match['odds'].items(), key=lambda x: float(x[1]['best_price']))
                matches_context += f"{best_odds[0]}: {best_odds[1]['best_price']} ({best_odds[1]['best_bookmaker']})\n\n"
            else:
                matches_context += "Sin cuotas disponibles\n\n"
        
        prompt = f"""
Analiza estas oportunidades de forma CONCISA:

{matches_context}

Responde en máximo 150 palabras con:

**Mejor Oportunidad**
El partido #1 más prometedor y por qué.

**Estrategia de Apuesta**
Cómo apostar y con qué bankroll.

**Alerta de Riesgo**
Un factor clave a vigilar.

Sé específico y directo.
"""
    
    response = model.generate_content(prompt)
    return response.text

def get_direct_match_data(home_team: str, away_team: str):
    """Get raw match data with all bookmakers for direct search"""
    
    print(f"\n{'='*60}")
    print(f"🔍 DIRECT SEARCH: {home_team} vs {away_team}")
    print(f"{'='*60}")
    
    odds_service = LiveOddsService()
    match_data = odds_service.get_match_analysis_data(home_team, away_team)
    
    if not match_data:
        odds_service.close()
        return None
    
    print(f"\n📊 MATCH FOUND:")
    print(f"   {match_data['home_team']} vs {match_data['away_team']}")
    print(f"   League: {match_data['league']}")
    print(f"   Kickoff: {match_data['kickoff']}")
    
    # Structure the data for frontend display
    structured_data = {
        "match_info": {
            "home_team": match_data['home_team'],
            "away_team": match_data['away_team'],
            "league": match_data['league'],
            "kickoff": match_data['kickoff']
        },
        "odds": {}
    }
    
    # Process odds for each outcome
    for outcome, data in match_data['odds'].items():
        structured_data["odds"][outcome] = {
            "best_price": data['best_price'],
            "best_bookmaker": data['best_bookmaker'],
            "all_bookmakers": data['all_bookmakers'],
            "average_price": sum([bm['price'] for bm in data['all_bookmakers']]) / len(data['all_bookmakers'])
        }
    
    odds_service.close()
    
    print(f"\n✅ DATA STRUCTURED FOR FRONTEND")
    return structured_data

def analyze_general_query(query: str):
    """Strict filtering - only soccer/betting topics allowed"""
    
    # More comprehensive soccer/betting keywords
    soccer_keywords = [
        # Spanish soccer terms
        'futbol', 'fútbol', 'equipo', 'partido', 'liga', 'jugador', 'entrenador', 
        'gol', 'campeonato', 'copa', 'champions', 'mundial', 'euro',
        'real madrid', 'barcelona', 'atletico', 'sevilla', 'valencia',
        'premier league', 'la liga', 'serie a', 'bundesliga', 'ligue 1',
        
        # English soccer terms  
        'football', 'soccer', 'team', 'match', 'league', 'player', 'coach',
        'goal', 'championship', 'world cup', 'uefa', 'fifa',
        
        # Betting terms
        'apuesta', 'apostar', 'bet', 'betting', 'cuota', 'cuotas', 'odds',
        'bookmaker', 'casa de apuestas', 'value bet', 'bankroll',
        'over', 'under', 'handicap', 'empate', 'draw', 'win', 'ganar',
        
        # Team names (add more as needed)
        'arsenal', 'chelsea', 'liverpool', 'manchester', 'city', 'united',
        'tottenham', 'newcastle', 'brighton', 'everton', 'leeds'
    ]
    
    query_lower = query.lower().strip()
    
    # Check if ANY soccer/betting keyword exists in the query
    is_soccer_related = any(keyword in query_lower for keyword in soccer_keywords)
    
    # Additional check for common non-soccer queries to reject
    non_soccer_keywords = [
        'cocina', 'cocinar', 'cook', 'cooking', 'receta', 'recipe', 'pasta', 'pastas',
        'comida', 'food', 'restaurant', 'música', 'music', 'película', 'movie',
        'tiempo', 'weather', 'trabajo', 'work', 'salud', 'health', 'medicina',
        'programación', 'programming', 'código', 'code', 'matemáticas', 'math'
    ]
    
    has_non_soccer_keywords = any(keyword in query_lower for keyword in non_soccer_keywords)
    
    # If it contains non-soccer keywords OR doesn't contain soccer keywords, reject
    if has_non_soccer_keywords or not is_soccer_related:
        return """
🤖 **Agente Especializado en Fútbol y Apuestas Deportivas**

Lo siento, soy un asistente especializado únicamente en:

⚽ **Fútbol**: Análisis de equipos, jugadores, partidos y competiciones
💰 **Apuestas Deportivas**: Cuotas, estrategias, value betting y recomendaciones  
📊 **Odds y Bookmakers**: Comparación de casas de apuestas y mercados

**Ejemplos de consultas que puedo ayudar:**
• "¿Cuáles son las mejores cuotas para el Real Madrid?"
• "Analiza el partido Liverpool vs Arsenal"
• "Dame estrategias de value betting"
• "¿Qué mercados recomiendas para la Premier League?"

Por favor, realiza una consulta relacionada con fútbol o apuestas deportivas.
"""
    
    # If it passes the filter, provide concise soccer/betting response
    prompt = f"""
Responde a esta consulta de fútbol/apuestas de forma CONCISA:

**CONSULTA**: {query}

Responde en máximo 120 palabras con información directa y útil.

Si es sobre:
- Equipos/jugadores: Situación actual y valor para apuestas
- Estrategias: Consejos prácticos y específicos  
- Predicciones: Análisis breve con justificación
- Mercados: Recomendaciones directas

Sé específico, práctico y enfocado en apuestas.
"""
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Test examples
    print("="*60)
    print("TEST 1: Análisis de equipo")
    print("="*60)
    print(analyze_team_with_live_odds("Inter Milan"))
    
    print("\n" + "="*60)
    print("TEST 2: Análisis de partido específico")
    print("="*60)
    print(analyze_specific_match("Real Madrid", "Juventus"))
    
    print("\n" + "="*60)
    print("TEST 3: Mejores apuestas de valor")
    print("="*60)
    print(get_best_value_bets(league="Premier League"))
    
    print("\n" + "="*60)
    print("TEST 4: Búsqueda directa de partido")
    print("="*60)
    print(get_direct_match_data("Barcelona", "Bayern Munich"))