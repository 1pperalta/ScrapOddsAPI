import React from 'react'

const MatchCard = ({ match, isSelected, onSelect }) => {
  // Calculate best odds for each outcome
  const outcomeOdds = {}
  match.bookmakers.forEach(bookie => {
    if (!outcomeOdds[bookie.outcome]) {
      outcomeOdds[bookie.outcome] = []
    }
    outcomeOdds[bookie.outcome].push({
      bookmaker: bookie.name,
      odds: bookie.odds,
      region: bookie.region
    })
  })

  // Get best odds for each outcome
  const bestOdds = {}
  Object.keys(outcomeOdds).forEach(outcome => {
    bestOdds[outcome] = outcomeOdds[outcome].reduce((best, current) => 
      current.odds > best.odds ? current : best
    )
  })

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getOutcomeEmoji = (outcome) => {
    switch (outcome.toLowerCase()) {
      case match.home.toLowerCase():
        return '🏠'
      case match.away.toLowerCase():
        return '✈️'
      case 'draw':
        return '🤝'
      default:
        return '⚽'
    }
  }

  return (
    <div 
      className={`card cursor-pointer transition-all duration-200 hover:shadow-xl ${
        isSelected ? 'ring-2 ring-premier-500 bg-premier-50' : 'hover:bg-gray-50'
      }`}
      onClick={onSelect}
    >
      {/* Match Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex-1">
          <div className="text-lg font-bold text-gray-800 mb-1">
            {match.home} vs {match.away}
          </div>
          <div className="text-sm text-gray-600">
            📅 {formatDate(match.kickoff)}
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500 mb-1">
            {match.bookmakers.length} bookmakers
          </div>
          <div className="text-xs text-premier-600 font-medium">
            Click for details
          </div>
        </div>
      </div>

      {/* Best Odds Preview */}
      <div className="grid grid-cols-3 gap-3">
        {Object.entries(bestOdds).map(([outcome, data]) => (
          <div key={outcome} className="text-center">
            <div className="text-xs text-gray-500 mb-1">
              {getOutcomeEmoji(outcome)} {outcome}
            </div>
            <div className="font-bold text-premier-600">
              {data.odds}
            </div>
            <div className="text-xs text-gray-400">
              {data.bookmaker}
            </div>
          </div>
        ))}
      </div>

      {/* Region Indicators */}
      <div className="mt-3 pt-3 border-t border-gray-100">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-500">Regions:</span>
          <div className="flex gap-1">
            {[...new Set(match.bookmakers.map(b => b.region))].map(region => (
              <span 
                key={region}
                className="px-2 py-1 bg-gray-100 rounded-full text-gray-600"
              >
                {region.toUpperCase()}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MatchCard
