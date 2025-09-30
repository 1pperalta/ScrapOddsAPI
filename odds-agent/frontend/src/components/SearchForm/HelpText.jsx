import React from 'react';
import { useSearchFormContext } from './SearchFormContext';

const HelpText = () => {
  const { searchType } = useSearchFormContext();

  return (
    <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-lg">
      {searchType === 'natural' ? (
        <div>
          <strong>💡 Natural Language Tips:</strong>
          <ul className="mt-1 space-y-1 ml-4">
            <li>• "What are the odds for Arsenal vs Chelsea?"</li>
            <li>• "Show me Manchester United's next match odds"</li>
            <li>• "Give me the best odds for Liverpool"</li>
          </ul>
        </div>
      ) : (
        <div>
          <strong>💡 Direct Search Tips:</strong>
          <ul className="mt-1 space-y-1 ml-4">
            <li>• Use format: "Team A vs Team B"</li>
            <li>• Examples: "Arsenal vs Chelsea", "Man City vs Liverpool"</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default HelpText;
