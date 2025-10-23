import React from 'react';
import { CalendarBlank } from 'phosphor-react';
import { formatMatchDate } from '../utils/dateFormatter';
import { calculateBestOdds } from '../utils/oddsCalculator';
import { getOutcomeIcon } from '../utils/iconHelpers';
import { TEXTS } from '../constants/texts';

const MatchCard = ({ match, isSelected, onSelect }) => {
  const bestOdds = calculateBestOdds(match.bookmakers);

  return (
    <div 
      className={`card cursor-pointer transition-all duration-200 hover:shadow-xl ${
        isSelected ? 'ring-2 ring-premier-500 bg-premier-50' : 'hover:bg-gray-50'
      }`}
      onClick={onSelect}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex-1">
          <div className="text-lg font-bold text-gray-800 mb-1">
            {match.home} vs {match.away}
          </div>
          <div className="text-sm text-gray-600 flex items-center gap-1">
            <CalendarBlank size={16} weight="duotone" /> {formatMatchDate(match.kickoff)}
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500 mb-1">
            {match.bookmakers.length} {TEXTS.matchCard.bookmakers}
          </div>
          <div className="text-xs text-premier-600 font-medium">
            {TEXTS.matchCard.clickForDetails}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        {Object.entries(bestOdds).map(([outcome, data]) => (
          <div key={outcome} className="text-center">
            <div className="text-xs text-gray-500 mb-1 flex items-center justify-center gap-1">
              {getOutcomeIcon(outcome, match.home, match.away, 14)} 
              <span>{outcome}</span>
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

      <div className="mt-3 pt-3 border-t border-gray-100">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-500">{TEXTS.matchCard.regions}</span>
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
  );
};

export default MatchCard;
