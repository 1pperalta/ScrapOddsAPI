import React, { useState } from 'react';
import { ChartBar, CalendarBlank, House, Airplane, Handshake, TrendUp } from 'phosphor-react';
import { formatMatchDateDetailed } from '../utils/dateFormatter';
import { calculateImpliedProbability, groupOddsByOutcome } from '../utils/oddsCalculator';
import { TEXTS } from '../constants/texts';

const OddsComparison = ({ match }) => {
  const [selectedOutcome, setSelectedOutcome] = useState(null);
  const oddsGrouped = groupOddsByOutcome(match.bookmakers);
  const outcomes = Object.keys(oddsGrouped);

  const getOutcomeColor = (outcome) => {
    switch (outcome.toLowerCase()) {
      case match.home.toLowerCase():
        return 'bg-green-50 border-green-200 text-green-800';
      case match.away.toLowerCase():
        return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'draw':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getOutcomeIcon = (outcome) => {
    if (outcome === match.home) return <House size={20} weight="fill" />;
    if (outcome === match.away) return <Airplane size={20} weight="fill" />;
    if (outcome.toLowerCase() === 'draw') return <Handshake size={20} weight="fill" />;
    return null;
  };

  return (
    <div className="card">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
          <ChartBar size={28} weight="duotone" className="text-premier-600" /> {TEXTS.oddsComparison.title}
        </h3>
        <div className="text-gray-600">
          <div className="font-medium text-lg">
            {match.home} vs {match.away}
          </div>
          <div className="text-sm flex items-center gap-1">
            <CalendarBlank size={16} weight="duotone" /> {formatMatchDateDetailed(match.kickoff)}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {outcomes.map(outcome => (
          <button
            key={outcome}
            onClick={() => setSelectedOutcome(
              selectedOutcome === outcome ? null : outcome
            )}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              selectedOutcome === outcome
                ? 'bg-premier-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {outcome} ({oddsGrouped[outcome].length})
          </button>
        ))}
      </div>

      <div className="space-y-6">
        {outcomes.map(outcome => {
          const isVisible = !selectedOutcome || selectedOutcome === outcome
          
          if (!isVisible) return null

          return (
            <div key={outcome} className={`border rounded-xl overflow-hidden ${getOutcomeColor(outcome)}`}>
              <div className="px-4 py-3 border-b border-current border-opacity-20">
                <h4 className="font-bold text-lg flex items-center gap-2">
                  {getOutcomeIcon(outcome)}
                  {outcome}
                </h4>
                <p className="text-sm opacity-75">
                  {TEXTS.oddsComparison.best}: {Math.max(...oddsGrouped[outcome].map(b => b.odds))} 
                  ({calculateImpliedProbability(Math.max(...oddsGrouped[outcome].map(b => b.odds)))}% {TEXTS.oddsComparison.implied})
                </p>
              </div>
              
              <div className="bg-white">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          {TEXTS.oddsComparison.bookmaker}
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          {TEXTS.oddsComparison.region}
                        </th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          {TEXTS.oddsComparison.odds}
                        </th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          {TEXTS.oddsComparison.impliedPercent}
                        </th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          {TEXTS.oddsComparison.rank}
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {oddsGrouped[outcome].map((bookie, index) => (
                        <tr 
                          key={`${bookie.name}-${index}`}
                          className={index === 0 ? 'bg-green-50' : 'hover:bg-gray-50'}
                        >
                          <td className="px-4 py-3">
                            <div className="font-medium text-gray-900">
                              {bookie.name}
                              {index === 0 && (
                                <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                                  {TEXTS.oddsComparison.best}
                                </span>
                              )}
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                              {bookie.region.toUpperCase()}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-premier-600">
                              {bookie.odds}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-gray-600">
                            {calculateImpliedProbability(bookie.odds)}%
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-medium ${
                              index === 0 
                                ? 'bg-gold-100 text-gold-800' 
                                : index < 3 
                                  ? 'bg-gray-100 text-gray-800'
                                  : 'bg-gray-50 text-gray-600'
                            }`}>
                              {index + 1}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <div className="mt-6 pt-6 border-t border-gray-200">
        <h5 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <TrendUp size={20} weight="duotone" className="text-premier-600" /> {TEXTS.oddsComparison.summaryTitle}
        </h5>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-gray-600">{TEXTS.oddsComparison.totalBookmakers}</div>
            <div className="font-bold text-lg">{match.bookmakers.length}</div>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-gray-600">{TEXTS.oddsComparison.regionsCovered}</div>
            <div className="font-bold text-lg">
              {[...new Set(match.bookmakers.map(b => b.region))].length}
            </div>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-gray-600">{TEXTS.oddsComparison.outcomesAvailable}</div>
            <div className="font-bold text-lg">{outcomes.length}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OddsComparison;
