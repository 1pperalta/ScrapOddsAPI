import axios from 'axios';

const API_BASE_URL = 'http://localhost:3001';

class GeminiAgent {
  async processQuery(naturalLanguageQuery) {
    try {
      console.log('🔍 Processing query:', naturalLanguageQuery);
      
      const queryType = this.determineQueryType(naturalLanguageQuery);
      
      let response;
      
      switch (queryType.type) {
        case 'team_analysis':
          response = await axios.post(`${API_BASE_URL}/api/agent/analyze-team`, {
            team: queryType.team
          });
          break;
          
        case 'match_analysis':
          response = await axios.post(`${API_BASE_URL}/api/agent/analyze-match`, {
            home_team: queryType.home_team,
            away_team: queryType.away_team
          });
          break;
          
        case 'value_bets':
        case 'best_bets':
        case 'weekend_bets':
        case 'general_betting':
          response = await axios.post(`${API_BASE_URL}/api/agent/value-bets`, {
            league: queryType.league,
            min_value_threshold: queryType.threshold || 1.05
          });
          break;
          
        default:
          // For any other query, try value bets as a fallback
          response = await axios.post(`${API_BASE_URL}/api/agent/value-bets`, {
            league: queryType.league || null,
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
    // Comprehensive league detection with Spanish and English synonyms
    const leaguePatterns = {
      'Premier League': [
        'premier', 'premier league', 'epl', 'english premier league',
        'liga inglesa', 'liga de inglaterra', 'inglaterra', 'liga premier',
        'futbol ingles', 'fútbol inglés'
      ],
      'La Liga': [
        'la liga', 'laliga', 'liga', 'spanish league', 'liga española',
        'liga de españa', 'españa', 'futbol español', 'fútbol español',
        'santander', 'primera división', 'primera division'
      ],
      'Serie A': [
        'serie a', 'seriea', 'italian league', 'liga italiana',
        'liga de italia', 'italia', 'futbol italiano', 'fútbol italiano',
        'calcio'
      ],
      'Bundesliga': [
        'bundesliga', 'german league', 'liga alemana',
        'liga de alemania', 'alemania', 'futbol aleman', 'fútbol alemán',
        'germania'
      ],
      'Ligue 1': [
        'ligue 1', 'ligue1', 'french league', 'liga francesa',
        'liga de francia', 'francia', 'futbol frances', 'fútbol francés',
        'ligue un'
      ],
      'Champions League': [
        'champions', 'champions league', 'ucl', 'uefa champions',
        'liga de campeones', 'champions league', 'orejona',
        'copa de europa', 'europea'
      ]
    };

    // Check each league's patterns
    for (const [leagueName, patterns] of Object.entries(leaguePatterns)) {
      for (const pattern of patterns) {
        if (queryLower.includes(pattern)) {
          return leagueName;
        }
      }
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