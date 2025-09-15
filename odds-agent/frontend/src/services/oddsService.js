import axios from 'axios'

const API_BASE_URL = '/api'

export const oddsService = {
  // Get odds for all matches or specific match
  async getOdds(matchQuery = null) {
    try {
      const params = matchQuery ? { match: matchQuery } : {}
      const response = await axios.get(`${API_BASE_URL}/odds`, { params })
      return response.data
    } catch (error) {
      console.error('Error fetching odds:', error)
      
      if (error.response?.status === 422) {
        throw new Error('Invalid request parameters. Please check your search.')
      } else if (error.response?.status === 429) {
        throw new Error('API rate limit exceeded. Please try again later.')
      } else if (error.response?.status === 401) {
        throw new Error('API authentication failed. Please check configuration.')
      } else {
        throw new Error('Failed to fetch odds. Please try again.')
      }
    }
  },

  // Get available teams
  async getTeams() {
    try {
      const response = await axios.get(`${API_BASE_URL}/teams`)
      return response.data
    } catch (error) {
      console.error('Error fetching teams:', error)
      throw new Error('Failed to fetch teams list.')
    }
  },

  // Get upcoming matches
  async getUpcomingMatches() {
    try {
      const response = await axios.get(`${API_BASE_URL}/matches`)
      return response.data
    } catch (error) {
      console.error('Error fetching matches:', error)
      throw new Error('Failed to fetch upcoming matches.')
    }
  }
}
