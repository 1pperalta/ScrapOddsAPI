import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import { createOddsRoutes } from './routes/odds.js'
import { createAgentRoutes } from './routes/agent.js'

// Load environment variables
dotenv.config()

const app = express()
const PORT = process.env.PORT || 5000

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.use('/api/odds', createOddsRoutes())
app.use('/api/agent', createAgentRoutes())

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  })
})

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err)
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  })
})

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path
  })
})

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`)
  console.log(`📊 Odds API: http://localhost:${PORT}/api/odds`)
  console.log(`🤖 Agent API: http://localhost:${PORT}/api/agent`)
})