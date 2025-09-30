import axios from 'axios';

const API_BASE_URL = '/api';

export const langGraphAgent = {
  async processQuery(naturalQuery) {
    try {
      const response = await axios.post(`${API_BASE_URL}/agent/process`, {
        query: naturalQuery
      });
      
      return response.data;
    } catch (error) {
      console.error('Error processing natural language query:', error);
      
      if (error.response?.status === 400) {
        throw new Error('Could not understand your query. Try being more specific about the match.');
      } else {
        throw new Error('AI agent is temporarily unavailable. Try using direct match search.');
      }
    }
  },

  async getSuggestions(partialQuery) {
    try {
      const response = await axios.post(`${API_BASE_URL}/agent/suggestions`, {
        query: partialQuery
      });
      
      return response.data.suggestions || [];
    } catch (error) {
      console.error('Error getting suggestions:', error);
      return [];
    }
  },

  async validateQuery(query) {
    try {
      const response = await axios.post(`${API_BASE_URL}/agent/validate`, {
        query: query
      });
      
      return response.data.isValid;
    } catch (error) {
      console.error('Error validating query:', error);
      return false;
    }
  }
};
