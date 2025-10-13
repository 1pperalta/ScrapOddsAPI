from dotenv import load_dotenv
import os
import google.generativeai as genai
from server_py.services.odds_service import LiveOddsService

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_team_with_live_odds(team: str):
    """Analyze team with real-time odds from PostgreSQL"""
    
    print(f"\n{'='*60}")
    print(f"🔍 FETCHING DATA FROM POSTGRESQL FOR: {team}")
    print(f"{'='*60}")
    
    odds_service = LiveOddsService()
    matches = odds_service.get_upcoming_matches_for_team(team, limit=5)
    
    print(f"\n📊 DATABASE QUERY RESULT:")
    print(f"   Found {len(matches)} matches")
    
    if not matches:
        odds_service.close()
        return f"❌ No hay partidos próximos disponibles para {team} en la base de datos."
    
    # Show raw data from database
    print(f"\n📋 RAW DATA FROM DATABASE:")
    for i, match in enumerate(matches, 1):
        print(f"\n   Match {i}:")
        print(f"   - League: {match['league']}")
        print(f"   - Teams: {match['home_team']} vs {match['away_team']}")
        print(f"   - Kickoff: {match['kickoff']}")
        print(f"   - Odds data: {len(match['odds'])} outcomes")
        for outcome, data in match['odds'].items():
            print(f"     * {outcome}: {data['best_price']} ({data['best_bookmaker']})")
    
    odds_service.close()
    
    print(f"\n{'='*60}")
    print(f"🤖 SENDING TO GEMINI FOR ANALYSIS...")
    print(f"{'='*60}\n")
    
    # Build context for Gemini
    context = f"🔴 ANÁLISIS EN VIVO PARA: {team}\n\n"
    context += f"📊 PRÓXIMOS {len(matches)} PARTIDOS CON CUOTAS EN TIEMPO REAL:\n\n"
    
    for i, match in enumerate(matches, 1):
        context += f"{'='*60}\n"
        context += f"PARTIDO {i}: {match['league']}\n"
        context += f"📅 {match['kickoff']}\n"
        context += f"⚽ {match['home_team']} vs {match['away_team']}\n\n"
        
        # Show best odds for each outcome
        context += "💰 MEJORES CUOTAS DISPONIBLES:\n"
        for outcome, data in match['odds'].items():
            context += f"  {outcome}: {data['best_price']} ({data['best_bookmaker']})\n"
            
            # Show comparison with other bookmakers
            if len(data['all_bookmakers']) > 1:
                other_odds = [b['price'] for b in data['all_bookmakers'] if b['bookmaker'] != data['best_bookmaker']]
                if other_odds:
                    avg_other = sum(other_odds) / len(other_odds)
                    value_diff = ((data['best_price'] - avg_other) / avg_other) * 100
                    context += f"    (Promedio otras casas: {avg_other:.2f}, diferencia: {value_diff:+.1f}%)\n"
        
        context += "\n"
    
    prompt = (
        f"Eres un analista experto en apuestas deportivas con acceso a datos en tiempo real.\n\n"
        f"{context}\n\n"
        f"Con base en esta información actualizada, proporciona:\n\n"
        f"1. **Análisis del equipo {team}**: Evalúa sus próximos partidos considerando rivales y condiciones.\n"
        f"2. **Evaluación de cuotas**: Identifica cuáles cuotas ofrecen valor real vs. expectativas.\n"
        f"3. **Oportunidades de apuesta**: Sugiere apuestas con mejor relación riesgo/beneficio.\n"
        f"4. **Estrategia recomendada**: Para cada partido, indica si apostar, evitar, o esperar mejores cuotas.\n"
        f"5. **Alertas de valor**: Si hay diferencias significativas entre bookmakers, señálalas.\n\n"
        f"Responde de forma profesional, concisa y orientada a la acción."
    )
    
    response = model.generate_content(prompt)
    
    print(f"\n{'='*60}")
    print(f"✅ GEMINI RESPONSE RECEIVED")
    print(f"{'='*60}\n")
    
    return response.text

def analyze_specific_match(home_team: str, away_team: str):
    """Analyze a specific upcoming match with live odds"""
    
    print(f"\n{'='*60}")
    print(f"🔍 FETCHING MATCH DATA FROM POSTGRESQL")
    print(f"{'='*60}")
    
    odds_service = LiveOddsService()
    match_data = odds_service.get_match_analysis_data(home_team, away_team)
    
    if not match_data:
        odds_service.close()
        return f"❌ No se encontró un partido próximo entre {home_team} y {away_team} en la base de datos."
    
    print(f"\n📊 DATABASE QUERY RESULT:")
    print(f"   Match found: {match_data['home_team']} vs {match_data['away_team']}")
    print(f"   League: {match_data['league']}")
    print(f"   Kickoff: {match_data['kickoff']}")
    print(f"   Odds outcomes: {len(match_data['odds'])}")
    
    for outcome, data in match_data['odds'].items():
        print(f"     * {outcome}: {data['best_price']} ({data['best_bookmaker']})")
    
    odds_service.close()
    
    print(f"\n{'='*60}")
    print(f"🤖 SENDING TO GEMINI FOR ANALYSIS...")
    print(f"{'='*60}\n")
    
    context = f"⚽ ANÁLISIS DE PARTIDO EN VIVO\n\n"
    context += f"{'='*60}\n"
    context += f"🏆 {match_data['league']}\n"
    context += f"📅 {match_data['kickoff']}\n"
    context += f"{match_data['home_team']} (Local) vs {match_data['away_team']} (Visitante)\n"
    context += f"{'='*60}\n\n"
    
    context += "💰 ANÁLISIS DE CUOTAS POR RESULTADO:\n\n"
    
    for outcome, data in match_data['odds'].items():
        context += f"📊 {outcome.upper()}\n"
        context += f"  Mejor cuota: {data['best_price']} en {data['best_bookmaker']}\n"
        context += f"  Bookmakers disponibles: {len(data['all_bookmakers'])}\n"
        
        # Calculate odds range
        all_prices = [b['price'] for b in data['all_bookmakers']]
        context += f"  Rango de cuotas: {min(all_prices):.2f} - {max(all_prices):.2f}\n"
        context += f"  Promedio mercado: {sum(all_prices)/len(all_prices):.2f}\n\n"
    
    prompt = (
        f"Eres un analista de apuestas deportivas con datos en tiempo real.\n\n"
        f"{context}\n\n"
        f"Proporciona un análisis detallado:\n\n"
        f"1. **Predicción del resultado**: ¿Qué resultado es más probable y por qué?\n"
        f"2. **Análisis de las cuotas**: ¿Las cuotas reflejan correctamente las probabilidades?\n"
        f"3. **Identificación de valor**: ¿Qué apuesta ofrece el mejor valor esperado?\n"
        f"4. **Comparación de bookmakers**: ¿Hay diferencias significativas que aprovechar?\n"
        f"5. **Recomendación final**: Apuesta sugerida con stake recomendado (1-5 unidades) y razón.\n\n"
        f"Sé específico, usa datos concretos y justifica tus recomendaciones."
    )
    
    response = model.generate_content(prompt)
    
    print(f"\n{'='*60}")
    print(f"✅ GEMINI RESPONSE RECEIVED")
    print(f"{'='*60}\n")
    
    return response.text

def get_best_value_bets(league=None, min_value_threshold=1.05):
    """Find matches with potential value bets across all games"""
    
    print(f"\n{'='*60}")
    print(f"🔍 SCANNING DATABASE FOR VALUE BETS")
    print(f"{'='*60}")
    if league:
        print(f"   League filter: {league}")
    print(f"   Min value threshold: {min_value_threshold}")
    
    odds_service = LiveOddsService()
    matches = odds_service.get_all_upcoming_matches(league=league, limit=20)
    
    print(f"\n📊 Found {len(matches)} upcoming matches to analyze")
    
    value_opportunities = []
    
    for match in matches:
        match_data = odds_service.get_match_analysis_data(
            match['home_team'], 
            match['away_team']
        )
        
        if not match_data:
            continue
        
        # Check for value in odds discrepancies
        for outcome, data in match_data['odds'].items():
            if len(data['all_bookmakers']) > 1:
                all_prices = [b['price'] for b in data['all_bookmakers']]
                avg_price = sum(all_prices) / len(all_prices)
                value_ratio = data['best_price'] / avg_price
                
                if value_ratio >= min_value_threshold:
                    value_opportunities.append({
                        "match": f"{match_data['home_team']} vs {match_data['away_team']}",
                        "league": match_data['league'],
                        "kickoff": match_data['kickoff'],
                        "outcome": outcome,
                        "best_odds": data['best_price'],
                        "best_bookmaker": data['best_bookmaker'],
                        "market_average": avg_price,
                        "value_percentage": (value_ratio - 1) * 100
                    })
    
    odds_service.close()
    
    print(f"\n💎 VALUE OPPORTUNITIES FOUND: {len(value_opportunities)}")
    
    if not value_opportunities:
        return "No se encontraron oportunidades de valor significativas en este momento."
    
    # Sort by value percentage
    value_opportunities.sort(key=lambda x: x['value_percentage'], reverse=True)
    
    print(f"\n{'='*60}")
    print(f"🤖 SENDING TO GEMINI FOR ANALYSIS...")
    print(f"{'='*60}\n")
    
    context = f"🎯 OPORTUNIDADES DE VALOR DETECTADAS\n\n"
    context += f"Se encontraron {len(value_opportunities)} apuestas con valor potencial:\n\n"
    
    for i, opp in enumerate(value_opportunities[:10], 1):  # Top 10
        context += f"{i}. {opp['match']} ({opp['league']})\n"
        context += f"   📅 {opp['kickoff']}\n"
        context += f"   💰 {opp['outcome']}: {opp['best_odds']} en {opp['best_bookmaker']}\n"
        context += f"   📊 Promedio mercado: {opp['market_average']:.2f}\n"
        context += f"   ✅ Valor: +{opp['value_percentage']:.1f}%\n\n"
    
    prompt = (
        f"Eres un analista de apuestas deportivas especializado en identificar valor.\n\n"
        f"{context}\n\n"
        f"Analiza estas oportunidades y proporciona:\n\n"
        f"1. **Top 3 recomendaciones**: Prioriza las mejores apuestas considerando valor Y probabilidad.\n"
        f"2. **Gestión de bankroll**: Sugiere stakes (1-5 unidades) para cada recomendación.\n"
        f"3. **Advertencias**: Señala riesgos o factores que podrían invalidar el valor aparente.\n"
        f"4. **Estrategia de ejecución**: ¿Apostar ahora o esperar? ¿Una sola casa o distribuir?\n\n"
        f"Sé conservador y profesional en tus recomendaciones."
    )
    
    response = model.generate_content(prompt)
    
    print(f"\n{'='*60}")
    print(f"✅ GEMINI RESPONSE RECEIVED")
    print(f"{'='*60}\n")
    
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