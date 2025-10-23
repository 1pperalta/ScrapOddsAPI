import axios from 'axios';

const API_BASE_URL = 'http://localhost:3001'; // Changed to 3001

class OddsService {
  async getOdds(query) {
    try {
      // Route through the agent instead
      const response = await axios.post(`${API_BASE_URL}/api/agent/process`, {
        query: query
      });

      return {
        analysis: response.data.analysis,
        confidence: response.data.confidence
      };
    } catch (error) {
      console.error('Error fetching odds:', error);
      throw new Error('Failed to fetch odds data. Please try again.');
    }
  }
}

export const oddsService = new OddsService();