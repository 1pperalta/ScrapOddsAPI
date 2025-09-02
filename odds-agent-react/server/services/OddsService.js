import axios from 'axios'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export class OddsService {
  constructor() {
    this.apiKey = process.env.ODDS_API_KEY
    this.sport = 'soccer_epl'
    this.regions = ['us', 'uk', 'au', 'eu']
    this.markets = 'h2h'
    
    if (!this.apiKey) {
      throw new Error('ODDS_API_KEY environment variable is required')
    }
  }

  async getOdds(matchFilter = null) {
    try {
      const allData = []
      
      // Fetch from all regions
      for (const region of this.regions) {
        try {
          const data = await this.fetchOddsFromRegion(region)
          if (data && data.length > 0) {
            // Add region info to each game
            data.forEach(game => {
              game.source_region = region
            })
            allData.push(...data)
          }
        } catch (error) {
          console.warn(`Failed to fetch odds from region ${region}:`, error.message)
        }
      }

      if (allData.length === 0) {
        console.log('⚠️ No live data available, using CSV data for testing')
        return this.getCSVOddsData(matchFilter)
      }

      // Flatten to the expected format
      const flattenedData = this.flattenOddsData(allData)
      
      // Filter by match if specified
      if (matchFilter) {
        return this.filterByMatch(flattenedData, matchFilter)
      }
      
      return flattenedData
    } catch (error) {
      console.log('⚠️ API error, falling back to CSV data:', error.message)
      return this.getCSVOddsData(matchFilter)
    }
  }

  async fetchOddsFromRegion(region) {
    const url = `https://api.the-odds-api.com/v4/sports/${this.sport}/odds`
    const params = {
      apiKey: this.apiKey,
      regions: region,
      markets: this.markets,
      oddsFormat: 'decimal'
    }

    try {
      const response = await axios.get(url, { 
        params,
        timeout: 30000 
      })
      
      console.log(`✅ Successfully fetched ${response.data.length} games from ${region}`)
      return response.data
    } catch (error) {
      if (error.response?.status === 422) {
        throw new Error(`Invalid API parameters for region ${region}`)
      } else if (error.response?.status === 429) {
        throw new Error('API rate limit exceeded')
      } else if (error.response?.status === 401) {
        throw new Error('Invalid API key')
      } else {
        throw new Error(`Failed to fetch odds from region ${region}: ${error.message}`)
      }
    }
  }

  flattenOddsData(data) {
    const rows = []
    
    for (const game of data) {
      const home = game.home_team
      const away = game.away_team
      const commence = game.commence_time
      const region = game.source_region || 'unknown'

      for (const book of game.bookmakers || []) {
        const bookie = book.title
        for (const market of book.markets || []) {
          for (const outcome of market.outcomes || []) {
            rows.push({
              home,
              away,
              kickoff: commence,
              region,
              bookmaker: bookie,
              outcome: outcome.name,
              odds: outcome.price
            })
          }
        }
      }
    }
    
    return rows
  }

  filterByMatch(oddsData, matchQuery) {
    const query = matchQuery.toLowerCase()
    
    return oddsData.filter(odd => {
      const homeTeam = odd.home.toLowerCase()
      const awayTeam = odd.away.toLowerCase()
      const matchString = `${homeTeam} vs ${awayTeam}`
      
      // Check various match formats
      return (
        matchString.includes(query) ||
        homeTeam.includes(query) ||
        awayTeam.includes(query) ||
        query.includes(homeTeam) ||
        query.includes(awayTeam)
      )
    })
  }

  async getTeams() {
    try {
      // Get odds data and extract unique teams
      const oddsData = await this.getOdds()
      const teams = new Set()
      
      oddsData.forEach(odd => {
        teams.add(odd.home)
        teams.add(odd.away)
      })
      
      return Array.from(teams).sort()
    } catch (error) {
      throw new Error(`Failed to fetch teams: ${error.message}`)
    }
  }

  async getUpcomingMatches() {
    try {
      const oddsData = await this.getOdds()
      const matchesMap = {}
      
      // Group by unique matches
      oddsData.forEach(odd => {
        const matchKey = `${odd.home}_vs_${odd.away}`
        if (!matchesMap[matchKey]) {
          matchesMap[matchKey] = {
            home: odd.home,
            away: odd.away,
            kickoff: odd.kickoff,
            bookmakers: new Set()
          }
        }
        matchesMap[matchKey].bookmakers.add(odd.bookmaker)
      })
      
      // Convert to array and sort by date
      return Object.values(matchesMap)
        .map(match => ({
          ...match,
          bookmakers: Array.from(match.bookmakers)
        }))
        .sort((a, b) => new Date(a.kickoff) - new Date(b.kickoff))
    } catch (error) {
      throw new Error(`Failed to fetch upcoming matches: ${error.message}`)
    }
  }

  getCSVOddsData(matchFilter = null) {
    try {
      const csvPath = path.join(__dirname, '../data/premier_league_odds.csv')
      
      if (!fs.existsSync(csvPath)) {
        console.error('CSV file not found:', csvPath)
        return []
      }

      const csvContent = fs.readFileSync(csvPath, 'utf-8')
      const lines = csvContent.trim().split('\n')
      const headers = lines[0].split(',')
      
      const oddsData = []
      
      for (let i = 1; i < lines.length; i++) {
        const values = this.parseCSVLine(lines[i])
        if (values.length === headers.length) {
          const record = {
            home: values[0],
            away: values[1], 
            kickoff: values[2],
            region: 'us', // Default region since CSV doesn't specify
            bookmaker: values[3],
            outcome: values[4],
            odds: parseFloat(values[5])
          }
          oddsData.push(record)
        }
      }
      
      // Filter by match if specified
      if (matchFilter) {
        const filtered = this.filterByMatch(oddsData, matchFilter)
        console.log(`📊 Returning ${filtered.length} CSV odds records for match: ${matchFilter}`)
        return filtered
      }
      
      console.log(`📊 Returning ${oddsData.length} CSV odds records from actual scraped data`)
      return oddsData
    } catch (error) {
      console.error('Error reading CSV file:', error)
      return this.getFallbackMockData(matchFilter)
    }
  }

  parseCSVLine(line) {
    const result = []
    let current = ''
    let inQuotes = false
    
    for (let i = 0; i < line.length; i++) {
      const char = line[i]
      
      if (char === '"') {
        inQuotes = !inQuotes
      } else if (char === ',' && !inQuotes) {
        result.push(current.trim())
        current = ''
      } else {
        current += char
      }
    }
    
    result.push(current.trim())
    return result
  }

  getFallbackMockData(matchFilter = null) {
    // Return empty data if CSV reading fails - we only want to show real scraped data
    console.log('⚠️ CSV file could not be read, returning empty data')
    return []
  }
}
