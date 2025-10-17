import React from 'react';

const DirectMatchDisplay = ({ matchData }) => {
  const { match_info, odds } = matchData;

  return (
    <div className="space-y-6">
      {/* Match Header */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-4">
          ⚽ {match_info.home_team} vs {match_info.away_team}
        </h2>
        <div className="text-gray-600 space-y-1">
          <p>🏆 <strong>Liga:</strong> {match_info.league}</p>
          <p>📅 <strong>Fecha:</strong> {new Date(match_info.kickoff).toLocaleString()}</p>
        </div>
      </div>

      {/* Odds Tables */}
      {Object.entries(odds).map(([outcome, data]) => (
        <div key={outcome} className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            📊 {outcome === 'home_win' ? `${match_info.home_team} Gana` : 
                 outcome === 'away_win' ? `${match_info.away_team} Gana` : 
                 'Empate'}
          </h3>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left p-3 font-medium">Casa de Apuestas</th>
                  <th className="text-right p-3 font-medium">Cuota</th>
                  <th className="text-right p-3 font-medium">Región</th>
                </tr>
              </thead>
              <tbody>
                {data.all_bookmakers
                  .sort((a, b) => b.price - a.price) // Sort by highest odds first
                  .map((bookmaker, index) => (
                  <tr 
                    key={index} 
                    className={`border-t ${bookmaker.bookmaker === data.best_bookmaker ? 'bg-green-50 border-green-200' : ''}`}
                  >
                    <td className="p-3">
                      {bookmaker.bookmaker === data.best_bookmaker && '👑 '}
                      {bookmaker.bookmaker}
                    </td>
                    <td className="text-right p-3 font-mono">
                      <span className={bookmaker.bookmaker === data.best_bookmaker ? 'text-green-600 font-bold' : ''}>
                        {bookmaker.price}
                      </span>
                    </td>
                    <td className="text-right p-3 text-gray-500">
                      {bookmaker.region || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-3 text-sm text-gray-600 bg-gray-50 p-3 rounded">
            📈 <strong>Promedio del mercado:</strong> {data.average_price.toFixed(2)}
          </div>
        </div>
      ))}
    </div>
  );
};

export default DirectMatchDisplay;