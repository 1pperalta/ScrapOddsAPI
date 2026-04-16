import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001';

class GeminiAgent {
  async processQuery(naturalLanguageQuery) {
    try {
      console.log('🔍 Processing query:', naturalLanguageQuery);
      
      const queryType = this.determineQueryType(naturalLanguageQuery);
      
      let response;
      
      switch (queryType.type) {
        case 'team_analysis':
          response = await axios.post(`${API_BASE_URL}/api/agent/analyze-team`, {
            team: queryType.team,
            query: naturalLanguageQuery
          });
          break;
          
        case 'match_analysis':
          response = await axios.post(`${API_BASE_URL}/api/agent/analyze-match`, {
            home_team: queryType.home_team,
            away_team: queryType.away_team,
            query: naturalLanguageQuery
          });
          break;
          
        case 'value_bets':
        case 'best_bets':
        case 'weekend_bets':
        case 'general_betting':
          response = await axios.post(`${API_BASE_URL}/api/agent/value-bets`, {
            league: queryType.league,
            query: naturalLanguageQuery,
            min_value_threshold: queryType.threshold || 1.05
          });
          break;
          
        default:
          // For any other query, try value bets as a fallback
          response = await axios.post(`${API_BASE_URL}/api/agent/value-bets`, {
            league: queryType.league || null,
            query: naturalLanguageQuery,
            min_value_threshold: 1.02 // Lower threshold for general queries
          });
      }
      
      console.log('✅ Backend response received:', {
        type: queryType.type,
        league: queryType.league,
        hasAnalysis: !!response.data.analysis
      });

      return {
        query: response.data.analysis || response.data.result,
        matchFound: true,
        confidence: response.data.confidence || 0.9,
        analysisType: queryType.type
      };
    } catch (error) {
      console.error('Error processing query with Gemini agent:', error);
      
      return {
        query: `Error: ${error.response?.data?.error || error.message}`,
        matchFound: false,
        confidence: 0.0
      };
    }
  }

  detectLeague(queryLower) {
    // Check specific leagues first to avoid substring matches
    // IMPORTANT: Check longer/more specific patterns before generic ones
    
    // Check Bundesliga first (before checking for 'liga')
    if (queryLower.includes('bundesliga')) {
      return 'Bundesliga';
    }
    
    // Check Ligue 1 (before checking for 'liga')
    if (queryLower.includes('ligue 1') || queryLower.includes('ligue1') || 
        (queryLower.includes('ligue') && queryLower.includes('frances'))) {
      return 'Ligue 1';
    }
    
    // Check Champions League
    if (queryLower.includes('champions') || queryLower.includes('campeones') || 
        queryLower.includes('ucl') || queryLower.includes('orejona')) {
      return 'Champions League';
    }
    
    // Check Premier League
    if (queryLower.includes('premier') || queryLower.includes('epl') ||
        queryLower.includes('liga inglesa') || queryLower.includes('liga de inglaterra')) {
      return 'Premier League';
    }
    
    // Check Serie A
    if (queryLower.includes('serie a') || queryLower.includes('seriea') ||
        queryLower.includes('liga italiana') || queryLower.includes('calcio')) {
      return 'Serie A';
    }
    
    // Check La Liga LAST (to avoid matching 'liga' in other leagues)
    if (queryLower.includes('la liga') || queryLower.includes('laliga') ||
        queryLower.includes('liga española') || queryLower.includes('liga de españa') ||
        queryLower.includes('santander') || queryLower.includes('primera división') ||
        queryLower.includes('primera division')) {
      return 'La Liga';
    }
    
    // Generic 'liga' only if no other league matched
    if (queryLower.includes('liga') && 
        !queryLower.includes('bundesliga') && 
        !queryLower.includes('ligue')) {
      return 'La Liga'; // Default to La Liga for generic 'liga' in Spanish context
    }

    return null; // No league detected
  }

  determineQueryType(query) {
    const lowerQuery = query.toLowerCase();
    
    // Check for team-specific queries FIRST (before value bets)
    const teamKeywords = ['equipo', 'por equipo', 'analiza', 'analyze', 'próximo partido', 'next match'];
    const hasTeamKeyword = teamKeywords.some(kw => lowerQuery.includes(kw));
    
    // Check for team analysis patterns
    const teamAnalysisPatterns = [
      /analiza\s+(.+)/i,  // "Analiza Real Madrid"
      /analyze (.+?) team/i,
      /(.+?) next matches/i,
      /upcoming games for (.+)/i,
      /(.+?) fixtures/i,
      /equipo\s+(.+)/i,  // "Equipo Arsenal"
      /por equipo\s+(.+)/i  // "Por equipo Manchester City"
    ];
    
    if (hasTeamKeyword) {
      for (const pattern of teamAnalysisPatterns) {
        const match = query.match(pattern);
        if (match && match[1]) {
          const teamName = match[1].trim();
          // Extract team name, remove "de la liga" type phrases
          const cleanTeam = teamName.replace(/\s+(de la|de|del|en)\s+.*/i, '');
          if (cleanTeam.split(' ').length <= 3) {
            return { type: 'team_analysis', team: cleanTeam };
          }
        }
      }
    }
    
    // Check for specific match analysis
    const matchPatterns = [
      /(.+?) vs (.+)/i,
      /(.+?) against (.+)/i,
      /match between (.+?) and (.+)/i
    ];
    
    for (const pattern of matchPatterns) {
      const match = query.match(pattern);
      if (match) {
        return { 
          type: 'match_analysis', 
          home_team: match[1].trim(), 
          away_team: match[2].trim() 
        };
      }
    }
    
    // Check for value/best bets queries (English & Spanish)
    const valueBetPatterns = [
      /value bet/i,
      /best bet/i,
      /best odds/i,
      /opportunities/i,
      /this weekend/i,
      /today/i,
      /tomorrow/i,
      /best match/i,
      /good bet/i,
      /recommended bet/i,
      /what to bet/i,
      /where to bet/i,
      /betting tip/i,
      /mejores apuestas/i,
      /mejor apuesta/i,
      /mejores cuotas/i,
      /mejor cuota/i,
      /oportunidades/i,
      /dame.*apuestas/i,
      /dame.*cuotas/i,
      /cuotas de/i,
      /apuestas de/i
    ];
    
    for (const pattern of valueBetPatterns) {
      if (pattern.test(lowerQuery)) {
        // Detect league with comprehensive Spanish synonyms
        const detectedLeague = this.detectLeague(lowerQuery);
        
        console.log('🎯 Detected value bets query for league:', detectedLeague || 'all leagues');
        
        return { 
          type: 'value_bets', 
          league: detectedLeague 
        };
      }
    }
    
    // If no specific pattern matches, default to value bets for betting-related queries
    const bettingKeywords = ['bet', 'odds', 'match', 'game', 'win', 'prediction', 'tip', 'apuesta', 'cuota'];
    if (bettingKeywords.some(keyword => lowerQuery.includes(keyword))) {
      const detectedLeague = this.detectLeague(lowerQuery);
      return { 
        type: 'general_betting',
        league: detectedLeague
      };
    }
    
    return { type: 'general', query: query };
  }

  async getDirectMatchData(homeTeam, awayTeam) {
    try {
      console.log('🔍 Direct search:', homeTeam, 'vs', awayTeam);
      
      const response = await axios.post(`${API_BASE_URL}/api/agent/direct-search`, {
        home_team: homeTeam,
        away_team: awayTeam
      });

      return {
        found: response.data.found,
        matchData: response.data.match_data,
        message: response.data.message
      };
    } catch (error) {
      console.error('Error in direct search:', error);
      return {
        found: false,
        matchData: null,
        message: error.response?.data?.message || 'Error al buscar el partido'
      };
    }
  }
}

export const geminiAgent = new GeminiAgent();