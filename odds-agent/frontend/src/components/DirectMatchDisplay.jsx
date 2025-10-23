import React, { useState } from 'react';

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
          <span className="text-2xl">📊</span>
          <h2 className="text-xl font-bold text-gray-500">
            Comparación Detallada de Cuotas
          </h2>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-gray-500">
            {match_info.home_team} vs {match_info.away_team}
          </h3>
          <div className="flex items-center gap-2 text-gray-500">
            <span>📅</span>
            <span className="text-sm">{formatDate(match_info.kickoff)}</span>
          </div>
        </div>

        {/* Outcome Tabs */}
        <div className="flex gap-2 mt-6">
          {Object.entries(odds).map(([outcome, data]) => (
            <button
              key={outcome}
              onClick={() => setActiveTab(outcome)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === outcome
                  ? 'bg-premier-500 text-white'
                  : 'bg-gray-500 text-white hover:bg-gray-500'
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
          <div className="flex items-center gap-2 mb-4">
            <span className="text-xl">✈️</span>
            <h3 className="text-lg font-semibold text-gray-500">
              {getOutcomeName(activeTab)}
            </h3>
            <span className="text-sm text-gray-500">
              Mejor: {odds[activeTab].best_price} ({Math.round(((1 / odds[activeTab].best_price) * 100) * 10) / 10}% implícita)
            </span>
          </div>

          {/* Bookmakers Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b-2 border-gray-500">
                  <th className="text-left py-3 px-4 font-medium text-gray-500">
                    CASA DE APUESTAS
                  </th>
                  <th className="text-center py-3 px-4 font-medium text-gray-500">
                    REGIÓN
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">
                    CUOTAS
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">
                    % IMPLÍCITO
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">
                    RANK
                  </th>
                </tr>
              </thead>
              <tbody>
                {getSortedBookmakers(odds[activeTab]).map((bookmaker, index) => (
                  <tr 
                    key={index}
                    className={`border-b border-gray-500 hover:bg-gray-50 ${
                      bookmaker.isBest ? 'bg-green-50 border-green-500' : ''
                    }`}
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        {bookmaker.isBest && (
                          <span className="text-green-500 font-bold text-xs bg-green-500 px-2 py-1 rounded text-white">
                            Mejor
                          </span>
                        )}
                        <span className={bookmaker.isBest ? 'font-semibold text-gray-500' : 'text-gray-500'}>
                          {bookmaker.bookmaker}
                        </span>
                      </div>
                    </td>
                    <td className="text-center py-3 px-4 text-gray-500">
                      {bookmaker.region || 'N/A'}
                    </td>
                    <td className="text-right py-3 px-4">
                      <span className={`font-mono ${
                        bookmaker.isBest 
                          ? 'text-premier-500 font-bold text-lg' 
                          : 'text-gray-500'
                      }`}>
                        {bookmaker.price}
                      </span>
                    </td>
                    <td className="text-right py-3 px-4 text-gray-500">
                      {getImplicitProbability(bookmaker.price)}%
                    </td>
                    <td className="text-right py-3 px-4">
                      <span className={`font-bold ${
                        bookmaker.rank === 1 
                          ? 'text-premier-500' 
                          : bookmaker.rank <= 3 
                            ? 'text-green-500' 
                            : 'text-gray-500'
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
          <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
            <div className="text-center">
              <div className="text-lg font-bold text-premier-500">
                {odds[activeTab].best_price}
              </div>
              <div className="text-xs text-gray-600">Mejor Cuota</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-green-500">
                {Math.round(odds[activeTab].average_price * 100) / 100}
              </div>
              <div className="text-xs text-gray-500">Promedio</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-purple-500">
                {getImplicitProbability(odds[activeTab].best_price)}%
              </div>
              <div className="text-xs text-gray-500">Prob. Implícita</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-gray-500">
                {odds[activeTab].all_bookmakers.length}
              </div>
              <div className="text-xs text-gray-500">Casas</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DirectMatchDisplay;