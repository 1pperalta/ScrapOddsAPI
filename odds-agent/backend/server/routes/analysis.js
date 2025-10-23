import express from 'express'
import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export function createAnalysisRoutes() {
  const router = express.Router()

  // Analyze team with live odds from PostgreSQL
  router.post('/team', async (req, res) => {
    try {
      const { team } = req.body
      
      if (!team) {
        return res.status(400).json({
          error: 'Team name is required'
        })
      }

      console.log(`🔍 Analyzing team: ${team}`)
      
      const result = await runPythonAgent('analyze_team', team)
      
      res.json({
        team,
        analysis: result.analysis,
        metadata: result.metadata || {},
        source: 'postgresql',
        timestamp: new Date().toISOString()
      })
    } catch (error) {
      console.error('Error analyzing team:', error)
      res.status(500).json({
        error: 'Failed to analyze team',
        message: error.message
      })
    }
  })

  // Analyze specific match
  router.post('/match', async (req, res) => {
    try {
      const { homeTeam, awayTeam } = req.body
      
      if (!homeTeam || !awayTeam) {
        return res.status(400).json({
          error: 'Both home and away team names are required'
        })
      }

      console.log(`⚽ Analyzing match: ${homeTeam} vs ${awayTeam}`)
      
      const result = await runPythonAgent('analyze_match', homeTeam, awayTeam)
      
      res.json({
        match: `${homeTeam} vs ${awayTeam}`,
        analysis: result.analysis,
        metadata: result.metadata || {},
        source: 'postgresql',
        timestamp: new Date().toISOString()
      })
    } catch (error) {
      console.error('Error analyzing match:', error)
      res.status(500).json({
        error: 'Failed to analyze match',
        message: error.message
      })
    }
  })

  // Get best value bets
  router.get('/value-bets', async (req, res) => {
    try {
      const { league } = req.query
      
      console.log(`💎 Finding value bets${league ? ` for ${league}` : ''}`)
      
      const result = await runPythonAgent('value_bets', league || '')
      
      res.json({
        analysis: result.analysis,
        metadata: result.metadata || {},
        league: league || 'all',
        source: 'postgresql',
        timestamp: new Date().toISOString()
      })
    } catch (error) {
      console.error('Error finding value bets:', error)
      res.status(500).json({
        error: 'Failed to find value bets',
        message: error.message
      })
    }
  })

  return router
}

// Helper function to run Python agent
function runPythonAgent(command, ...args) {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, '../../server_py/api_wrapper.py')
    
    const pythonProcess = spawn('python3', [
      pythonScript,
      command,
      ...args.filter(arg => arg) // Remove empty args
    ])

    let output = ''
    let errorOutput = ''

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${errorOutput}`))
      } else {
        try {
          // Parse JSON output from Python
          const result = JSON.parse(output)
          resolve(result)
        } catch (error) {
          // If not JSON, return raw output
          resolve({ analysis: output })
        }
      }
    })

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`))
    })
  })
}