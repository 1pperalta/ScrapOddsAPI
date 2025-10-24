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

# Safety settings - Allow betting/gambling content
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

# System instruction to balance analysis with data grounding
system_instruction = """You are a professional sports betting analyst.

CRITICAL RULES:
1. ONLY mention matches explicitly shown in the context
2. ONLY use the exact odds, bookmakers, and prices provided
3. DO NOT mix information between different matches
4. DO NOT invent or imagine matches, odds, or bookmakers
5. Keep each match analysis separate and clear
6. Use clean, professional language WITHOUT emojis

RESPONSE STYLE:
- Direct and professional
- Structured and organized
- Spanish language
- No emojis or excessive formatting
- Maximum 250 words"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",  # Stable model
    generation_config=generation_config,
    safety_settings=safety_settings,
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
            
            if match.get('odds') and len(match['odds']) > 0:
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
Análisis profesional de {team} para apuestas deportivas.

FORMATO DE RESPUESTA REQUERIDO (usa markdown):

## SITUACIÓN DE {team.upper()}
[2 líneas: momento actual del equipo]

## PRÓXIMOS PARTIDOS

**1. {team} vs [Rival]**
- Fecha: [fecha]
- Cuota victoria: [precio] ([Bookmaker])
- Valoración: [Buena/Regular/Mala]

**2. {team} vs [Rival]**
- Fecha: [fecha]
- Cuota victoria: [precio] ([Bookmaker])
- Valoración: [Buena/Regular/Mala]

## RECOMENDACIONES
- [Recomendación específica 1]
- [Recomendación específica 2]

## GESTIÓN
- Riesgo: [Bajo/Medio/Alto]
- Distribución: [específica]

Usa EXACTAMENTE este formato. Máximo 200 palabras.
"""
    
    try:
        response = model.generate_content(prompt)
        if not response.candidates or not response.candidates[0].content.parts:
            return f"⚠️ No se pudo generar análisis para {team}. Por favor, intenta de nuevo."
        return response.text
    except Exception as e:
        print(f"❌ Error in analyze_team_with_live_odds: {e}")
        return f"❌ Error al analizar {team}: {str(e)}"

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
    
    try:
        response = model.generate_content(prompt)
        if not response.candidates or not response.candidates[0].content.parts:
            analysis_text = f"⚠️ No se pudo generar análisis para {home_team} vs {away_team}"
        else:
            analysis_text = response.text
    except Exception as e:
        print(f"❌ Error in analyze_specific_match: {e}")
        analysis_text = f"❌ Error al analizar el partido: {str(e)}"
    
    return {
        'analysis': analysis_text,
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
        # Build detailed context with TOP 3 matches (to avoid overwhelming Gemini)
        matches_context = f"📊 **DATOS REALES DE LA BASE DE DATOS**\n"
        matches_context += f"Fecha actual: {current_date}\n"
        matches_context += f"Liga filtro: {league_filter}\n"
        matches_context += f"Partidos totales: {len(matches)} | Mostrando los 3 mejores\n\n"
        
        for i, match in enumerate(matches[:3], 1):
            matches_context += f"**PARTIDO {i}**: {match['home_team']} vs {match['away_team']}\n"
            matches_context += f"📅 {match['kickoff']} | 🏆 {match['league']}\n"
            
            if match.get('odds') and len(match['odds']) > 0:
                matches_context += f"**Cuotas:**\n"
                for outcome, data in match['odds'].items():
                    matches_context += f"  • {outcome}: {data['best_price']} ({data['best_bookmaker']})\n"
            else:
                matches_context += "  • Sin cuotas\n"
            matches_context += "\n"
        
        prompt = f"""
Analiza SOLO los partidos mostrados abajo para encontrar oportunidades de value betting.

FECHA: {current_date}
LIGA: {league_filter}

{matches_context}

REGLAS ESTRICTAS:
- SOLO menciona los partidos listados arriba
- NO inventes partidos o cuotas
- SOLO usa las cuotas exactas mostradas
- Sé específico con bookmaker y precio

FORMATO DE RESPUESTA REQUERIDO (usa markdown para estructura clara):

## TOP OPORTUNIDADES

**1. [Equipo Local] vs [Equipo Visitante]**
- Apuesta: [Resultado]
- Cuota: [precio] ([Bookmaker])
- Razón: [1 línea de por qué]

**2. [Equipo Local] vs [Equipo Visitante]**
- Apuesta: [Resultado]
- Cuota: [precio] ([Bookmaker])
- Razón: [1 línea de por qué]

## ANÁLISIS
[2-3 líneas cortas de análisis general]

## GESTIÓN
- Distribuir: [recomendación específica]
- Riesgo: [nivel bajo/medio/alto]

Usa EXACTAMENTE este formato. Máximo 200 palabras.
"""
    
    try:
        response = model.generate_content(prompt)
        
        # Check if response has valid content
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"⚠️ Gemini API returned empty response. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'unknown'}")
            return f"""
❌ **Error al generar análisis**

El sistema de IA no pudo generar una respuesta en este momento.

**Datos disponibles:**
{len(matches)} partidos encontrados para {league_filter}

Por favor, intenta:
1. Reformular tu consulta
2. Verificar que hay partidos en la base de datos (ejecuta el scrapper)
3. Intentar más tarde

"""
        
        return response.text
        
    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        return f"""
❌ **Error en el análisis**

Hubo un problema al generar el análisis de apuestas.

**Datos disponibles:** {len(matches)} partidos de {league_filter}

Error técnico: {str(e)}

Por favor, intenta de nuevo o contacta soporte.
"""

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
    
    try:
        response = model.generate_content(prompt)
        if not response.candidates or not response.candidates[0].content.parts:
            return "⚠️ No se pudo generar respuesta. Por favor, reformula tu consulta."
        return response.text
    except Exception as e:
        print(f"❌ Error in analyze_general_query: {e}")
        return f"❌ Error al procesar la consulta: {str(e)}"

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