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
            league: null,
            min_value_threshold: 1.02 // Lower threshold for general queries
          });
      }

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

  determineQueryType(query) {
    const lowerQuery = query.toLowerCase();
    
    // Check for team analysis patterns
    const teamAnalysisPatterns = [
      /analyze (.+?) team/i,
      /(.+?) next matches/i,
      /upcoming games for (.+)/i,
      /(.+?) fixtures/i,
      /^([a-zA-Z\s]+)$/i  // Single team name
    ];
    
    for (const pattern of teamAnalysisPatterns) {
      const match = query.match(pattern);
      if (match && match[1] && match[1].trim().split(' ').length <= 3) { // Prevent long sentences from matching
        return { type: 'team_analysis', team: match[1].trim() };
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
    
    // Check for value/best bets queries
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
      /betting tip/i
    ];
    
    for (const pattern of valueBetPatterns) {
      if (pattern.test(lowerQuery)) {
        const leagueMatch = query.match(/in (.+?) league/i) || 
                           query.match(/(premier league|la liga|serie a|bundesliga|ligue 1|champions league)/i);
        return { 
          type: 'value_bets', 
          league: leagueMatch ? leagueMatch[1] : null 
        };
      }
    }
    
    // If no specific pattern matches, default to value bets for betting-related queries
    const bettingKeywords = ['bet', 'odds', 'match', 'game', 'win', 'prediction', 'tip'];
    if (bettingKeywords.some(keyword => lowerQuery.includes(keyword))) {
      return { type: 'general_betting' };
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