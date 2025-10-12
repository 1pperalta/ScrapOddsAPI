import axios from 'axios';
import { TEXTS } from '../constants/texts';

const API_BASE_URL = '/api';

export const oddsService = {
  async getOdds(matchQuery = null) {
    try {
      const params = matchQuery ? { match: matchQuery } : {};
      const response = await axios.get(`${API_BASE_URL}/odds`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching odds:', error);
      
      if (error.response?.status === 422) {
        throw new Error(TEXTS.errors.invalidRequest);
      } else if (error.response?.status === 429) {
        throw new Error(TEXTS.errors.rateLimit);
      } else if (error.response?.status === 401) {
        throw new Error(TEXTS.errors.authFailed);
      } else {
        throw new Error(TEXTS.errors.fetchFailed);
      }
    }
  },

  async getTeams() {
    try {
      const response = await axios.get(`${API_BASE_URL}/teams`);
      return response.data;
    } catch (error) {
      console.error('Error fetching teams:', error);
      throw new Error(TEXTS.errors.teamsFetchFailed);
    }
  },

  async getUpcomingMatches() {
    try {
      const response = await axios.get(`${API_BASE_URL}/matches`);
      return response.data;
    } catch (error) {
      console.error('Error fetching matches:', error);
      throw new Error(TEXTS.errors.matchesFetchFailed);
    }
  }
};
