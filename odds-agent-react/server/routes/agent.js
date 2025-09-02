import express from 'express'
import { LangGraphOddsAgent } from '../services/LangGraphOddsAgent.js'

export function createAgentRoutes() {
  const router = express.Router()
  const agent = new LangGraphOddsAgent()

  // Process natural language query
  router.post('/process', async (req, res) => {
    try {
      const { query } = req.body
      
      if (!query || typeof query !== 'string') {
        return res.status(400).json({
          error: 'Invalid query',
          message: 'Query must be a non-empty string'
        })
      }

      console.log(`🤖 Processing natural language query: "${query}"`)
      
      const result = await agent.processQuery(query)
      
      res.json(result)
    } catch (error) {
      console.error('Error processing query:', error)
      res.status(500).json({
        error: 'Failed to process query',
        message: error.message
      })
    }
  })

  // Get suggestions for partial queries
  router.post('/suggestions', async (req, res) => {
    try {
      const { query } = req.body
      
      if (!query || typeof query !== 'string') {
        return res.status(400).json({
          error: 'Invalid query',
          message: 'Query must be a non-empty string'
        })
      }

      const suggestions = await agent.getSuggestions(query)
      
      res.json({ suggestions })
    } catch (error) {
      console.error('Error getting suggestions:', error)
      res.status(500).json({
        error: 'Failed to get suggestions',
        suggestions: []
      })
    }
  })

  // Validate if query is about Premier League
  router.post('/validate', async (req, res) => {
    try {
      const { query } = req.body
      
      if (!query || typeof query !== 'string') {
        return res.status(400).json({
          error: 'Invalid query',
          message: 'Query must be a non-empty string'
        })
      }

      const isValid = await agent.validateQuery(query)
      
      res.json({ isValid })
    } catch (error) {
      console.error('Error validating query:', error)
      res.status(500).json({
        error: 'Failed to validate query',
        isValid: false
      })
    }
  })

  return router
}
