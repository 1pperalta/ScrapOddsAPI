import React from 'react';
import { useSearchFormContext } from './SearchFormContext';

const ModeToggle = () => {
  const { searchType, setSearchType } = useSearchFormContext();

  return (
    <div className="flex items-center space-x-4">
      <span className="text-sm font-medium text-gray-700">Search mode:</span>
      <div className="flex space-x-2">
        <button
          type="button"
          onClick={() => setSearchType('natural')}
          className={`px-3 py-1 rounded-full text-sm transition-colors ${
            searchType === 'natural'
              ? 'bg-premier-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          🤖 Natural Language
        </button>
        <button
          type="button"
          onClick={() => setSearchType('direct')}
          className={`px-3 py-1 rounded-full text-sm transition-colors ${
            searchType === 'direct'
              ? 'bg-premier-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          📝 Direct Match
        </button>
      </div>
    </div>
  );
};

export default ModeToggle;
