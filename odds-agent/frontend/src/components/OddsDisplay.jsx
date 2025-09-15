import React, { useState } from 'react'
import MatchCard from './MatchCard'
import OddsComparison from './OddsComparison'

const OddsDisplay = ({ oddsData, selectedMatch, onMatchSelect }) => {
  const [sortBy, setSortBy] = useState('date')
  const [filterBy, setFilterBy] = useState('all')

  if (!oddsData || oddsData.length === 0) {
    return (
      <div className="card text-center">
        <div className="text-gray-500">
          <h3 className="text-lg font-semibold mb-2">No matches found</h3>
          <p>Try searching for a different match or check your search terms.</p>
        </div>
      </div>
    )
  }

  // Group odds data by match
  const matchesMap = {}
  oddsData.forEach(odd => {
    const matchKey = `${odd.home}_vs_${odd.away}`
    if (!matchesMap[matchKey]) {
      matchesMap[matchKey] = {
        home: odd.home,
        away: odd.away,
        kickoff: odd.kickoff,
        bookmakers: []
      }
    }
    matchesMap[matchKey].bookmakers.push({
      name: odd.bookmaker,
      region: odd.region,
      outcome: odd.outcome,
      odds: odd.odds
    })
  })

  const matches = Object.values(matchesMap)

  // Sort matches
  const sortedMatches = [...matches].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(a.kickoff) - new Date(b.kickoff)
      case 'home':
        return a.home.localeCompare(b.home)
      case 'away':
        return a.away.localeCompare(b.away)
      default:
        return 0
    }
  })

  return (
    <div className="space-y-6">
      {/* Results Header */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-800">
              📊 Odds Results
            </h2>
            <p className="text-gray-600">
              Found {matches.length} match{matches.length !== 1 ? 'es' : ''}
            </p>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="date">Sort by Date</option>
              <option value="home">Sort by Home Team</option>
              <option value="away">Sort by Away Team</option>
            </select>
          </div>
        </div>
      </div>

      {/* Matches Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {sortedMatches.map((match, index) => (
          <MatchCard
            key={index}
            match={match}
            isSelected={selectedMatch && 
              selectedMatch.home === match.home && 
              selectedMatch.away === match.away
            }
            onSelect={() => onMatchSelect(match)}
          />
        ))}
      </div>

      {/* Detailed Odds Comparison */}
      {selectedMatch && (
        <OddsComparison match={selectedMatch} />
      )}
    </div>
  )
}

export default OddsDisplay
