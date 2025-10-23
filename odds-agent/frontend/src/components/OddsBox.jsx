import React from 'react';

const OddsBox = ({ matchData }) => {
  const { match_info, odds } = matchData;

  return (
    <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4 mb-4">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-800">
          {match_info?.home_team || 'Team 1'} vs {match_info?.away_team || 'Team 2'}
        </h3>
        <div className="text-right text-sm text-gray-600">
          <div>{match_info?.bookmaker_count || 0} casas de apuestas</div>
          <div className="text-premier-500 cursor-pointer">Clic para detalles</div>
        </div>
      </div>
      
      <div className="flex items-center text-sm text-gray-600 mb-4">
        📅 {match_info?.kickoff || 'Fecha TBD'}
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        {/* Home Win */}
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            🏠 <span className="ml-1 text-gray-700">{match_info?.home_team || 'Local'}</span>
          </div>
          <div className="text-2xl font-bold text-premier-500">
            {odds?.home_win?.best_price || 'N/A'}
          </div>
          <div className="text-xs text-gray-500">
            {odds?.home_win?.best_bookmaker || ''}
          </div>
        </div>
        
        {/* Away Win */}
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            ✈️ <span className="ml-1 text-gray-700">{match_info?.away_team || 'Visitante'}</span>
          </div>
          <div className="text-2xl font-bold text-premier-500">
            {odds?.away_win?.best_price || 'N/A'}
          </div>
          <div className="text-xs text-gray-500">
            {odds?.away_win?.best_bookmaker || ''}
          </div>
        </div>
        
        {/* Draw */}
        <div className="text-center">
          <div className="flex items-center justify-center mb-1">
            🤝 <span className="ml-1 text-gray-700">Empate</span>
          </div>
          <div className="text-2xl font-bold text-premier-500">
            {odds?.draw?.best_price || 'N/A'}
          </div>
          <div className="text-xs text-gray-500">
            {odds?.draw?.best_bookmaker || ''}
          </div>
        </div>
      </div>
      
      {match_info?.league && (
        <div className="mt-3 text-center text-sm text-gray-600">
          🏆 {match_info.league}
        </div>
      )}
    </div>
  );
};

export default OddsBox;