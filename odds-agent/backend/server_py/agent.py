from dotenv import load_dotenv
import os
from datetime import datetime
import google.generativeai as genai
from server_py.services.odds_service import LiveOddsService

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure model for balanced analysis
generation_config = {
    "temperature": 0.5,  # Balanced: factual but allows intelligent analysis
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1500,  # Allow longer, more detailed responses
}

# System instruction to balance analysis with data grounding
system_instruction = """You are a professional sports betting analyst with deep knowledge of football.

YOUR ROLE:
- Provide intelligent, insightful analysis
- Use your football knowledge to evaluate teams, form, and matchups
- Compare odds to identify value betting opportunities
- Give strategic betting advice

DATA INTEGRITY RULES:
1. When discussing specific matches/odds, ONLY use data from the provided context
2. You can analyze teams generally (form, tactics, strengths) using football knowledge
3. When making betting recommendations, reference specific odds from the context
4. If asked about a match not in the data, say "No tengo datos de ese partido"
5. Be honest about data limitations

RESPONSE STYLE:
- Analytical and professional
- Specific when discussing odds
- Strategic when giving betting advice
- Use Spanish for responses
- Balance data with football insights"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

def analyze_team_with_live_odds(team: str):
    """Concise team analysis focused on betting value"""
    
    odds_service = LiveOddsService()
    matches = odds_service.get_upcoming_matches_for_team(team, limit=3)
    odds_service.close()
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Build detailed odds context
    if matches:
        odds_context = f"📊 **DATOS REALES DE LA BASE DE DATOS**\n"
        odds_context += f"Fecha actual: {current_date}\n"
        odds_context += f"Partidos encontrados: {len(matches)}\n\n"
        
        for i, match in enumerate(matches, 1):
            odds_context += f"**PARTIDO {i}**: {match['home_team']} vs {match['away_team']}\n"
            odds_context += f"📅 Fecha: {match['kickoff']}\n"
            odds_context += f"🏆 Competición: {match['league']}\n"
            odds_context += f"**Cuotas disponibles:**\n"
            
            if match.get('odds'):
                for outcome, data in match['odds'].items():
                    odds_context += f"  • {outcome}: {data['best_price']} (Bookmaker: {data['best_bookmaker']})\n"
            else:
                odds_context += "  • Sin cuotas disponibles para este partido\n"
            odds_context += "\n"
    else:
        odds_context = f"❌ **NO HAY DATOS EN LA BASE DE DATOS**\n"
        odds_context += f"No se encontraron partidos próximos para '{team}' en la base de datos.\n"
        odds_context += f"El equipo puede no estar en nuestro sistema o no tener partidos programados.\n"
    
    prompt = f"""
Eres un analista profesional de fútbol y apuestas deportivas. Tu trabajo es proporcionar análisis inteligente basado en datos reales.

FECHA Y HORA ACTUAL: {current_date}

DATOS DISPONIBLES:
{odds_context}

INSTRUCCIONES:
1. Usa los datos proporcionados como FUNDAMENTO de tu análisis
2. Puedes hacer análisis inteligente, comparar cuotas, identificar valor
3. Puedes discutir forma del equipo, contexto, rivalidades
4. PERO siempre referencia las cuotas específicas cuando hagas recomendaciones
5. Si mencionas un partido, debe estar en los datos arriba

TAREA:
Proporciona un análisis profesional de {team} para apuestas deportivas.

FORMATO DE RESPUESTA:

**⚽ Situación de {team}**
Evaluación concisa de su momento actual y próximos desafíos (basándote en los rivales listados).

**💰 Análisis de Cuotas y Recomendaciones**
- Evalúa las cuotas específicas mostradas
- Identifica cuáles ofrecen valor y por qué
- Compara entre bookmakers si hay diferencias
- Sugiere estrategias de apuesta específicas

**🎯 Predicción y Estrategia**
- Pronóstico para los partidos listados
- Gestión de bankroll recomendada
- Factores clave a vigilar

Sé analítico, específico y útil. Máximo 300 palabras.
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
    matches = odds_service.get_all_upcoming_matches(league=league, limit=10)
    odds_service.close()
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    league_filter = league if league else "todas las ligas"
    
    if not matches:
        return f"""
❌ **No hay datos disponibles para {league_filter}**

No se encontraron partidos próximos en la base de datos para esta liga.

**Posibles razones:**
• El scrapper no se ha ejecutado recientemente
• No hay partidos programados en los próximos días
• La liga seleccionada no está en nuestro sistema

**Ligas disponibles en el sistema:**
• Premier League (Inglaterra)
• La Liga (España)
• Serie A (Italia)
• Bundesliga (Alemania)
• Ligue 1 (Francia)
• Champions League

**Sugerencias:**
1. Intenta con otra liga: "Mejores apuestas de La Liga"
2. Ejecuta el scrapper para actualizar los datos
3. Pregunta por equipos específicos: "Analiza Arsenal"
"""
    else:
        # Build detailed context with ALL odds
        matches_context = f"📊 **DATOS REALES DE LA BASE DE DATOS**\n"
        matches_context += f"Fecha actual: {current_date}\n"
        matches_context += f"Liga filtro: {league_filter}\n"
        matches_context += f"Partidos encontrados: {len(matches)}\n\n"
        
        for i, match in enumerate(matches[:5], 1):
            matches_context += f"**PARTIDO {i}**: {match['home_team']} vs {match['away_team']}\n"
            matches_context += f"📅 {match['kickoff']} | 🏆 {match['league']}\n"
            
            if match.get('odds') and len(match['odds']) > 0:
                matches_context += f"**Cuotas disponibles:**\n"
                for outcome, data in match['odds'].items():
                    matches_context += f"  • {outcome}: {data['best_price']} ({data['best_bookmaker']})\n"
            else:
                matches_context += "  • Sin cuotas disponibles\n"
            matches_context += "\n"
        
        prompt = f"""
Eres un analista experto en value betting. Tu trabajo es identificar las mejores oportunidades de apuesta basándote en análisis de cuotas y conocimiento de fútbol.

FECHA ACTUAL: {current_date}
LIGA: {league_filter}

PARTIDOS DISPONIBLES:
{matches_context}

TAREA:
Analiza estos {len(matches)} partidos y encuentra las mejores oportunidades de value betting.

FORMATO DE RESPUESTA:

**🎯 Oportunidades Destacadas**
Identifica las 2-3 mejores apuestas:
- Partido y cuota específica (con bookmaker)
- ¿Por qué esta cuota ofrece valor?
- ¿Qué factores del partido la hacen atractiva?

**💰 Análisis de Valor**
- Compara las cuotas entre bookmakers si hay diferencias
- Identifica cuotas que parecen sobrevaloradas o infravaloradas
- Explica el razonamiento táctico/situacional

**📊 Estrategia de Bankroll**
- Cómo distribuir las apuestas
- Gestión de riesgo recomendada
- Apuestas simples vs combinadas

**⚠️ Consideraciones Clave**
Factores importantes a tener en cuenta en estos partidos específicos

Sé analítico y específico. Máximo 350 palabras.
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