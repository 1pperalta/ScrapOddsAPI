import React, { useState } from 'react';
import { ChartBar } from 'phosphor-react';
import { useProcessedMatches } from '../hooks/useProcessedMatches';
import MatchCard from './MatchCard';
import OddsComparison from './OddsComparison';
import { TEXTS } from '../constants/texts';

const OddsDisplay = ({ oddsData }) => {
  const [selectedMatch, setSelectedMatch] = useState(null);
  const { sortedMatches, sortBy, setSortBy, matchesCount } = useProcessedMatches(oddsData);

  if (!oddsData || oddsData.length === 0) {
    return (
      <div className="card text-center">
        <div className="text-gray-500">
          <h3 className="text-lg font-semibold mb-2">{TEXTS.oddsDisplay.noMatchesFound}</h3>
          <p>{TEXTS.oddsDisplay.tryDifferentSearch}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
              <ChartBar size={24} weight="duotone" className="text-premier-600" /> {TEXTS.oddsDisplay.title}
            </h2>
            <p className="text-gray-600">
              {TEXTS.oddsDisplay.foundMatches} {matchesCount} {matchesCount !== 1 ? TEXTS.oddsDisplay.matches : TEXTS.oddsDisplay.match}
            </p>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="date">{TEXTS.oddsDisplay.sortByDate}</option>
              <option value="home">{TEXTS.oddsDisplay.sortByHome}</option>
              <option value="away">{TEXTS.oddsDisplay.sortByAway}</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {sortedMatches.map((match, index) => (
          <MatchCard
            key={index}
            match={match}
            isSelected={selectedMatch && 
              selectedMatch.home === match.home && 
              selectedMatch.away === match.away
            }
            onSelect={() => setSelectedMatch(match)}
          />
        ))}
      </div>

      {selectedMatch && (
        <OddsComparison match={selectedMatch} />
      )}
    </div>
  );
};

export default OddsDisplay;
