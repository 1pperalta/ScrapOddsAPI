from dotenv import load_dotenv
import os
from datetime import datetime
import google.generativeai as genai
from server_py.services.odds_service import LiveOddsService
from server_py.services.rag_service import get_rag_service

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
system_instruction = """You are a professional sports analyst providing market analysis.

CRITICAL FORMATTING RULES:
1. NEVER use emojis or special characters (no trophy, ball, chart icons)
2. MAXIMUM 3 matches per response
3. Use clean markdown: ## for titles, **bold** for emphasis
4. Keep structure consistent across all responses
5. Spanish language, professional tone

DATA RULES:
1. ONLY mention matches explicitly shown in the context
2. ONLY use exact odds, bookmakers, and prices provided
3. DO NOT invent matches, odds, or bookmakers
4. Keep each match analysis separate and clear

RESPONSE STYLE:
- Clean, structured markdown
- Professional and direct
- Maximum 200 words
- No decorative characters"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",  # Stable model
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_instruction
)

def analyze_team_with_live_odds(team: str):
    """Concise team analysis focused on betting value with RAG context"""
    
    # Get odds data
    odds_service = LiveOddsService()
    matches = odds_service.get_upcoming_matches_for_team(team, limit=3)
    odds_service.close()
    
    # Get team context from RAG
    rag_service = get_rag_service()
    team_contexts = rag_service.retrieve_team_context(team, top_k=1)
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Build team context section
    if team_contexts:
        rag_context = f"\n**CONTEXTO DEL EQUIPO (Datos actualizados):**\n"
        rag_context += rag_service.format_context_for_prompt(team_contexts)
        rag_context += "\n"
    else:
        rag_context = ""
    
    # Build detailed odds context
    if matches:
        odds_context = f"**PRÓXIMOS PARTIDOS Y CUOTAS:**\n"
        odds_context += f"Fecha actual: {current_date}\n"
        odds_context += f"Partidos encontrados: {len(matches)}\n\n"
        
        for i, match in enumerate(matches, 1):
            odds_context += f"**PARTIDO {i}**: {match['home_team']} vs {match['away_team']}\n"
            odds_context += f"Fecha: {match['kickoff']}\n"
            odds_context += f"Competición: {match['league']}\n"
            odds_context += f"**Cuotas disponibles:**\n"
            
            if match.get('odds') and len(match['odds']) > 0:
                for outcome, data in match['odds'].items():
                    odds_context += f"  • {outcome}: {data['best_price']} (Bookmaker: {data['best_bookmaker']})\n"
            else:
                odds_context += "  • Sin cuotas disponibles para este partido\n"
            odds_context += "\n"
    else:
        odds_context = f"**NO HAY PARTIDOS PRÓXIMOS**\n"
        odds_context += f"No se encontraron partidos próximos para '{team}' en la base de datos.\n"
        odds_context += f"El equipo puede no estar en nuestro sistema o no tener partidos programados.\n"
    
    prompt = f"""
Analiza {team} basándote EXCLUSIVAMENTE en los datos proporcionados.

FECHA ACTUAL: {current_date}

{rag_context}

{odds_context}

FORMATO OBLIGATORIO (sin emojis, máximo 3 partidos):

## ANALISIS DE {team.upper()}

**Situación actual:** [1-2 líneas sobre forma y posición según datos RAG]

## PROXIMOS PARTIDOS

**1. [Local] vs [Visitante]**
- Fecha: [exacta del dato]
- Probabilidad victoria {team}: [precio] ([Bookmaker])
- Valoracion: [Favorable/Neutra/Desfavorable]

**2. [Local] vs [Visitante]**
- Fecha: [exacta del dato]
- Probabilidad victoria {team}: [precio] ([Bookmaker])
- Valoracion: [Favorable/Neutra/Desfavorable]

**3. [Local] vs [Visitante]**
- Fecha: [exacta del dato]
- Probabilidad victoria {team}: [precio] ([Bookmaker])
- Valoracion: [Favorable/Neutra/Desfavorable]

## CONCLUSION

[2 líneas: mejor opción según probabilidades y contexto deportivo]

IMPORTANTE: NO uses emojis. Solo texto y markdown limpio. Máximo 180 palabras.
"""
    
    try:
        response = model.generate_content(prompt)
        if not response.candidates or not response.candidates[0].content.parts:
            return f"## ERROR\n\nNo se pudo generar análisis para {team}. Por favor, intenta de nuevo."
        return response.text
    except Exception as e:
        print(f"ERROR in analyze_team_with_live_odds: {e}")
        return f"## ERROR\n\nError al analizar {team}: {str(e)}"

def analyze_specific_match(home_team: str, away_team: str):
    """Concise match analysis for betting with RAG context"""
    
    # Get match odds
    match_data = get_direct_match_data(home_team, away_team)
    
    # Get team contexts from RAG
    rag_service = get_rag_service()
    match_context = rag_service.retrieve_match_context(home_team, away_team, top_k_per_team=1)
    
    # Build RAG context section
    rag_context = rag_service.format_match_context_for_prompt(match_context)
    
    # Build odds context
    if match_data:
        odds_context = f"\n**CUOTAS DISPONIBLES**:\n"
        odds_context += f"Fecha: {match_data['match_info']['kickoff']} | Competición: {match_data['match_info']['league']}\n\n"
        for outcome, data in match_data['odds'].items():
            odds_context += f"• **{outcome}**: {data['best_price']} ({data['best_bookmaker']})\n"
        odds_context += "\n"
    else:
        odds_context = "\nNo hay cuotas específicas disponibles.\n\n"
    
    prompt = f"""
Analiza el partido {home_team} vs {away_team} usando SOLO los datos proporcionados.

{rag_context}

{odds_context}

FORMATO OBLIGATORIO (sin emojis):

## ANALISIS: {home_team.upper()} vs {away_team.upper()}

**Factor clave:** [1 línea sobre el aspecto deportivo decisivo]

## PROBABILIDADES DE MERCADO

**Victoria {home_team}:** [precio] ([Bookmaker])
- Valoracion: [Análisis breve basado en forma]

**Empate:** [precio] ([Bookmaker])
- Valoracion: [Análisis breve]

**Victoria {away_team}:** [precio] ([Bookmaker])
- Valoracion: [Análisis breve basado en forma]

## CONCLUSION

[2 líneas: resultado más probable y mejor opción según datos]

IMPORTANTE: NO uses emojis. Máximo 150 palabras.
"""
    
    try:
        response = model.generate_content(prompt)
        if not response.candidates or not response.candidates[0].content.parts:
            analysis_text = f"## ERROR\n\nNo se pudo generar análisis para {home_team} vs {away_team}"
        else:
            analysis_text = response.text
    except Exception as e:
        print(f"ERROR in analyze_specific_match: {e}")
        analysis_text = f"## ERROR\n\nError al analizar el partido: {str(e)}"
    
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
## NO HAY DATOS DISPONIBLES

No se encontraron partidos próximos para {league_filter} en la base de datos.

**Posibles razones:**
- El scrapper no se ha ejecutado recientemente
- No hay partidos programados en los próximos días
- La liga seleccionada no está en nuestro sistema

**Ligas disponibles:**
- Premier League (Inglaterra)
- La Liga (España)
- Serie A (Italia)
- Bundesliga (Alemania)
- Ligue 1 (Francia)
- Champions League

**Sugerencias:**
1. Intenta con otra liga
2. Ejecuta el scrapper para actualizar datos
3. Pregunta por equipos específicos
"""
    else:
        # Build detailed context with TOP 3 matches (to avoid overwhelming Gemini)
        matches_context = f"**DATOS DE LA BASE DE DATOS**\n"
        matches_context += f"Fecha actual: {current_date}\n"
        matches_context += f"Liga: {league_filter}\n"
        matches_context += f"Partidos totales: {len(matches)} | Mostrando los 3 mejores\n\n"
        
        for i, match in enumerate(matches[:3], 1):
            matches_context += f"**PARTIDO {i}**: {match['home_team']} vs {match['away_team']}\n"
            matches_context += f"Fecha: {match['kickoff']} | Liga: {match['league']}\n"
            
            if match.get('odds') and len(match['odds']) > 0:
                matches_context += f"**Probabilidades:**\n"
                for outcome, data in match['odds'].items():
                    matches_context += f"  - {outcome}: {data['best_price']} ({data['best_bookmaker']})\n"
            else:
                matches_context += "  - Sin probabilidades disponibles\n"
            matches_context += "\n"
        
        prompt = f"""
Analiza los partidos de {league_filter} usando EXCLUSIVAMENTE los datos mostrados.

FECHA: {current_date}

{matches_context}

FORMATO OBLIGATORIO (sin emojis, máximo 3 partidos):

## MEJORES OPCIONES - {league_filter.upper()}

**1. [Local] vs [Visitante]**
- Fecha: [exacta]
- Opcion recomendada: [Victoria Local/Empate/Victoria Visitante]
- Probabilidad: [precio] ([Bookmaker])
- Razon: [1 línea justificación deportiva]

**2. [Local] vs [Visitante]**
- Fecha: [exacta]
- Opcion recomendada: [Victoria Local/Empate/Victoria Visitante]
- Probabilidad: [precio] ([Bookmaker])
- Razon: [1 línea justificación deportiva]

**3. [Local] vs [Visitante]**
- Fecha: [exacta]
- Opcion recomendada: [Victoria Local/Empate/Victoria Visitante]
- Probabilidad: [precio] ([Bookmaker])
- Razon: [1 línea justificación deportiva]

## RESUMEN

**Nivel de confianza:** [Alto/Medio/Bajo]
**Distribucion sugerida:** [Descripción breve]

IMPORTANTE: NO uses emojis. SOLO los 3 primeros partidos. Máximo 180 palabras.
"""
    
    try:
        response = model.generate_content(prompt)
        
        # Check if response has valid content
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"WARNING: Gemini API returned empty response. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'unknown'}")
            return f"""
## ERROR AL GENERAR ANALISIS

El sistema no pudo generar una respuesta en este momento.

**Datos disponibles:** {len(matches)} partidos de {league_filter}

**Por favor intenta:**
1. Reformular tu consulta
2. Verificar que hay partidos (ejecuta el scrapper)
3. Intentar más tarde
"""
        
        return response.text
        
    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        return f"""
## ERROR EN EL ANALISIS

Hubo un problema al generar el análisis.

**Datos disponibles:** {len(matches)} partidos de {league_filter}

**Error técnico:** {str(e)}

Por favor, intenta de nuevo.
"""

def get_direct_match_data(home_team: str, away_team: str):
    """Get raw match data with all bookmakers for direct search"""
    
    print(f"\n{'='*60}")
    print(f"DIRECT SEARCH: {home_team} vs {away_team}")
    print(f"{'='*60}")
    
    odds_service = LiveOddsService()
    match_data = odds_service.get_match_analysis_data(home_team, away_team)
    
    if not match_data:
        odds_service.close()
        return None
    
    print(f"\nMATCH FOUND:")
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
    
    print(f"\nDATA STRUCTURED FOR FRONTEND")
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
## AGENTE ESPECIALIZADO EN FUTBOL Y ANALISIS DEPORTIVO

Lo siento, soy un asistente especializado únicamente en:

**Futbol:** Análisis de equipos, jugadores, partidos y competiciones
**Analisis Deportivo:** Estadísticas, estrategias y recomendaciones  
**Mercados:** Comparación de casas de apuestas y probabilidades

**Ejemplos de consultas:**
- Cuales son las mejores probabilidades para el Real Madrid
- Analiza el partido Liverpool vs Arsenal
- Dame estrategias de analisis deportivo
- Que mercados recomiendas para la Premier League

Por favor, realiza una consulta relacionada con futbol o analisis deportivo.
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
            return "## ERROR\n\nNo se pudo generar respuesta. Por favor, reformula tu consulta."
        return response.text
    except Exception as e:
        print(f"ERROR in analyze_general_query: {e}")
        return f"## ERROR\n\nError al procesar la consulta: {str(e)}"

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