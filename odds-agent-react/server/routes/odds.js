import express from 'express'
import { OddsService } from '../services/OddsService.js'

export function createOddsRoutes() {
  const router = express.Router()
  const oddsService = new OddsService()

  // Get all odds or filtered by match
  router.get('/', async (req, res) => {
    try {
      const { match } = req.query
      
      console.log(`📊 Fetching odds${match ? ` for: ${match}` : ' for all matches'}`)
      
      const odds = await oddsService.getOdds(match)
      
      res.json(odds)
    } catch (error) {
      console.error('Error in odds route:', error)
      
      if (error.message.includes('422')) {
        res.status(422).json({
          error: 'Invalid API request',
          message: 'Check your API key and parameters'
        })
      } else if (error.message.includes('rate limit')) {
        res.status(429).json({
          error: 'Rate limit exceeded',
          message: 'Please try again later'
        })
      } else {
        res.status(500).json({
          error: 'Failed to fetch odds',
          message: error.message
        })
      }
    }
  })

  // Get available teams
  router.get('/teams', async (req, res) => {
    try {
      const teams = await oddsService.getTeams()
      res.json(teams)
    } catch (error) {
      console.error('Error fetching teams:', error)
      res.status(500).json({
        error: 'Failed to fetch teams',
        message: error.message
      })
    }
  })

  // Get upcoming matches
  router.get('/matches', async (req, res) => {
    try {
      const matches = await oddsService.getUpcomingMatches()
      res.json(matches)
    } catch (error) {
      console.error('Error fetching matches:', error)
      res.status(500).json({
        error: 'Failed to fetch matches',
        message: error.message
      })
    }
  })

  return router
}
