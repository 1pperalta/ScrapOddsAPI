import React, { useState } from 'react';
import { ChartBar, Calendar, Trophy, Target } from 'phosphor-react';

const DirectMatchDisplay = ({ matchData }) => {
  const { match_info, odds } = matchData;
  const [activeTab, setActiveTab] = useState(Object.keys(odds)[0] || 'home_win');

  // Format outcome names for display
  const getOutcomeName = (outcome) => {
    switch (outcome) {
      case 'home_win':
        return match_info.home_team;
      case 'away_win':
        return match_info.away_team;
      case 'draw':
        return 'Draw';
      default:
        return outcome;
    }
  };

  // Calculate implicit probability percentage
  const getImplicitProbability = (odds) => {
    return ((1 / odds) * 100).toFixed(1);
  };

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Sort bookmakers by odds (highest first) and add ranking
  const getSortedBookmakers = (outcomeData) => {
    return outcomeData.all_bookmakers
      .sort((a, b) => b.price - a.price)
      .map((bookmaker, index) => ({
        ...bookmaker,
        rank: index + 1,
        isBest: bookmaker.bookmaker === outcomeData.best_bookmaker
      }));
  };

  return (
    <div className="space-y-6">
      {/* Match Header */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <ChartBar size={24} weight="duotone" className="text-premier-500" />
          <h2 className="text-xl font-bold text-dark">
            Comparación Detallada de Cuotas
          </h2>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-dark">
            {match_info.home_team} vs {match_info.away_team}
          </h3>
          <div className="flex items-center gap-2 text-dark">
            <Calendar size={18} weight="duotone" className="text-premier-500" />
            <span className="text-base">{formatDate(match_info.kickoff)}</span>
          </div>
        </div>

        {/* Outcome Tabs */}
        <div className="flex gap-2 mt-6 flex-wrap">
          {Object.entries(odds).map(([outcome, data]) => (
            <button
              key={outcome}
              onClick={() => setActiveTab(outcome)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors text-base ${
                activeTab === outcome
                  ? 'bg-premier-500 text-white shadow-md'
                  : 'bg-gray-500 text-white hover:bg-premier-500'
              }`}
            >
              {getOutcomeName(outcome)} ({Math.round(odds[outcome].average_price * 10) / 10})
            </button>
          ))}
        </div>
      </div>

      {/* Active Tab Content */}
      {odds[activeTab] && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            <Target size={24} weight="duotone" className="text-premier-500" />
            <h3 className="text-lg font-semibold text-dark">
              {getOutcomeName(activeTab)}
            </h3>
            <span className="text-base text-dark">
              Mejor: {odds[activeTab].best_price} ({Math.round(((1 / odds[activeTab].best_price) * 100) * 10) / 10}% implícita)
            </span>
          </div>

          {/* Bookmakers Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-base">
              <thead>
                <tr className="border-b-2 border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-dark">
                    CASA DE APUESTAS
                  </th>
                  <th className="text-center py-3 px-4 font-semibold text-dark">
                    REGIÓN
                  </th>
                  <th className="text-right py-3 px-4 font-semibold text-dark">
                    CUOTAS
                  </th>
                  <th className="text-right py-3 px-4 font-semibold text-dark">
                    % IMPLÍCITO
                  </th>
                  <th className="text-right py-3 px-4 font-semibold text-dark">
                    RANK
                  </th>
                </tr>
              </thead>
              <tbody>
                {getSortedBookmakers(odds[activeTab]).map((bookmaker, index) => (
                  <tr 
                    key={index}
                    className={`border-b border-gray-200 hover:bg-gray-50 transition-colors ${
                      bookmaker.isBest ? 'bg-green-50' : ''
                    }`}
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        {bookmaker.isBest && (
                          <span className="text-white font-semibold text-xs bg-green-500 px-2 py-1 rounded">
                            Mejor
                          </span>
                        )}
                        <span className={`text-base ${bookmaker.isBest ? 'font-semibold text-dark' : 'text-dark'}`}>
                          {bookmaker.bookmaker}
                        </span>
                      </div>
                    </td>
                    <td className="text-center py-3 px-4 text-dark text-base">
                      {bookmaker.region || 'N/A'}
                    </td>
                    <td className="text-right py-3 px-4">
                      <span className={`font-mono text-base font-bold ${
                        bookmaker.isBest 
                          ? 'text-premier-500' 
                          : 'text-dark'
                      }`}>
                        {bookmaker.price}
                      </span>
                    </td>
                    <td className="text-right py-3 px-4 text-dark text-base">
                      {getImplicitProbability(bookmaker.price)}%
                    </td>
                    <td className="text-right py-3 px-4">
                      <span className={`font-bold text-base ${
                        bookmaker.rank === 1 
                          ? 'text-premier-500' 
                          : bookmaker.rank <= 3 
                            ? 'text-green-500' 
                            : 'text-dark'
                      }`}>
                        {bookmaker.rank}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Summary Stats */}
          <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="text-center">
              <div className="text-lg font-bold text-premier-500">
                {odds[activeTab].best_price}
              </div>
              <div className="text-sm text-dark">Mejor Cuota</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-green-500">
                {Math.round(odds[activeTab].average_price * 100) / 100}
              </div>
              <div className="text-sm text-dark">Promedio</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-purple-500">
                {getImplicitProbability(odds[activeTab].best_price)}%
              </div>
              <div className="text-sm text-dark">Prob. Implícita</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-dark">
                {odds[activeTab].all_bookmakers.length}
              </div>
              <div className="text-sm text-dark">Casas</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DirectMatchDisplay;