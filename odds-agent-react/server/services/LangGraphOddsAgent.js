import axios from 'axios'

export class LangGraphOddsAgent {
  constructor() {
    this.huggingFaceApiKey = process.env.HUGGING_FACE_API_KEY
    this.model = "microsoft/DialoGPT-medium" // Free model
    
    // Premier League teams for validation
    this.premierLeagueTeams = [
      'Arsenal', 'Aston Villa', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace',
      'Everton', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 
      'Manchester United', 'Newcastle', 'Nottingham Forest', 'Sheffield United',
      'Tottenham', 'West Ham', 'Wolves', 'Bournemouth', 'Brentford'
    ]

    // Common team aliases
    this.teamAliases = {
      'man city': 'Manchester City',
      'man utd': 'Manchester United',
      'man united': 'Manchester United',
      'spurs': 'Tottenham',
      'arsenal': 'Arsenal',
      'chelsea': 'Chelsea',
      'liverpool': 'Liverpool',
      'newcastle': 'Newcastle',
      'brighton': 'Brighton'
    }
  }

  async processQuery(naturalQuery) {
    try {
      console.log(`🤖 Processing: "${naturalQuery}"`)
      
      // First, try simple pattern matching for common queries
      const simpleMatch = this.simpleMatchExtraction(naturalQuery)
      if (simpleMatch.matchFound) {
        return simpleMatch
      }

      // If available, use Hugging Face for more complex queries
      if (this.huggingFaceApiKey) {
        return await this.processWithHuggingFace(naturalQuery)
      } else {
        // Fallback to rule-based processing
        return this.ruleBasedProcessing(naturalQuery)
      }
    } catch (error) {
      console.error('Error processing query:', error)
      
      // Fallback to rule-based processing
      return this.ruleBasedProcessing(naturalQuery)
    }
  }

  simpleMatchExtraction(query) {
    const normalizedQuery = query.toLowerCase()
    
    // Look for "vs", "against", "v" patterns
    const vsPatterns = [
      /(.+?)\s+(?:vs|v|against|playing)\s+(.+)/,
      /(.+?)\s+(?:odds|match|game)\s+(?:vs|v|against)\s+(.+)/,
      /(?:odds for|show me)\s+(.+?)\s+(?:vs|v|against)\s+(.+)/
    ]

    for (const pattern of vsPatterns) {
      const match = normalizedQuery.match(pattern)
      if (match) {
        const team1 = this.normalizeTeamName(match[1].trim())
        const team2 = this.normalizeTeamName(match[2].trim())
        
        if (this.isValidTeam(team1) && this.isValidTeam(team2)) {
          const matchQuery = `${team1} vs ${team2}`
          return {
            query: matchQuery,
            matchFound: true,
            confidence: 0.9,
            teams: [team1, team2],
            method: 'pattern_matching'
          }
        }
      }
    }

    // Look for single team mentions
    for (const team of this.premierLeagueTeams) {
      if (normalizedQuery.includes(team.toLowerCase())) {
        return {
          query: team,
          matchFound: true,
          confidence: 0.7,
          teams: [team],
          method: 'single_team'
        }
      }
    }

    // Check aliases
    for (const [alias, fullName] of Object.entries(this.teamAliases)) {
      if (normalizedQuery.includes(alias)) {
        return {
          query: fullName,
          matchFound: true,
          confidence: 0.8,
          teams: [fullName],
          method: 'alias_matching'
        }
      }
    }

    return { matchFound: false }
  }

  async processWithHuggingFace(query) {
    try {
      // Create a structured prompt for team extraction
      const prompt = `Extract Premier League team names from this query: "${query}". Teams: Arsenal, Chelsea, Liverpool, Manchester City, Manchester United, Tottenham, etc. Response format: Team1 vs Team2 or just Team1.`
      
      const response = await axios.post(
        `https://api-inference.huggingface.co/models/${this.model}`,
        {
          inputs: prompt,
          parameters: {
            max_length: 50,
            temperature: 0.3
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${this.huggingFaceApiKey}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000
        }
      )

      const generatedText = response.data[0]?.generated_text || ''
      console.log('🤖 HuggingFace response:', generatedText)
      
      // Extract teams from the generated response
      const extractedMatch = this.simpleMatchExtraction(generatedText)
      if (extractedMatch.matchFound) {
        return {
          ...extractedMatch,
          method: 'huggingface',
          originalQuery: query
        }
      }
      
      // Fallback to rule-based
      return this.ruleBasedProcessing(query)
    } catch (error) {
      console.warn('HuggingFace API failed, using fallback:', error.message)
      return this.ruleBasedProcessing(query)
    }
  }

  ruleBasedProcessing(query) {
    const normalizedQuery = query.toLowerCase()
    
    // Try to find any team mentions
    const mentionedTeams = []
    
    for (const team of this.premierLeagueTeams) {
      if (normalizedQuery.includes(team.toLowerCase())) {
        mentionedTeams.push(team)
      }
    }

    // Check aliases
    for (const [alias, fullName] of Object.entries(this.teamAliases)) {
      if (normalizedQuery.includes(alias) && !mentionedTeams.includes(fullName)) {
        mentionedTeams.push(fullName)
      }
    }

    if (mentionedTeams.length >= 2) {
      return {
        query: `${mentionedTeams[0]} vs ${mentionedTeams[1]}`,
        matchFound: true,
        confidence: 0.8,
        teams: mentionedTeams.slice(0, 2),
        method: 'rule_based_multiple'
      }
    } else if (mentionedTeams.length === 1) {
      return {
        query: mentionedTeams[0],
        matchFound: true,
        confidence: 0.6,
        teams: mentionedTeams,
        method: 'rule_based_single'
      }
    }

    return {
      matchFound: false,
      confidence: 0,
      error: 'Could not identify Premier League teams in your query',
      suggestions: [
        'Try: "Arsenal vs Chelsea"',
        'Try: "Show me odds for Liverpool"',
        'Try: "Man City vs Tottenham odds"'
      ]
    }
  }

  normalizeTeamName(teamName) {
    const normalized = teamName.trim()
    
    // Check if it's an alias
    const alias = this.teamAliases[normalized.toLowerCase()]
    if (alias) return alias
    
    // Find partial matches
    for (const team of this.premierLeagueTeams) {
      if (team.toLowerCase().includes(normalized.toLowerCase()) || 
          normalized.toLowerCase().includes(team.toLowerCase())) {
        return team
      }
    }
    
    return normalized
  }

  isValidTeam(teamName) {
    return this.premierLeagueTeams.some(team => 
      team.toLowerCase() === teamName.toLowerCase()
    )
  }

  async getSuggestions(partialQuery) {
    const normalizedQuery = partialQuery.toLowerCase()
    const suggestions = []

    // Find teams that match the partial query
    for (const team of this.premierLeagueTeams) {
      if (team.toLowerCase().includes(normalizedQuery)) {
        suggestions.push(`${team} odds`)
        suggestions.push(`${team} vs Chelsea`)
        suggestions.push(`Show me ${team} match odds`)
      }
    }

    // Add some common suggestions
    if (normalizedQuery.includes('arsenal')) {
      suggestions.push('Arsenal vs Chelsea', 'Arsenal vs Tottenham')
    }
    if (normalizedQuery.includes('liverpool')) {
      suggestions.push('Liverpool vs Manchester City', 'Liverpool vs Arsenal')
    }

    return suggestions.slice(0, 5)
  }

  async validateQuery(query) {
    const processed = await this.processQuery(query)
    return processed.matchFound && processed.confidence > 0.5
  }
}
