import React from 'react';
import { useSearchFormContext } from './SearchFormContext';

const quickSearchOptions = [
  'Arsenal vs Chelsea',
  'Manchester United vs Liverpool',
  'Manchester City vs Tottenham',
  'Newcastle vs Brighton'
];

const QuickSearch = () => {
  const { setQuery, loading } = useSearchFormContext();

  return (
    <div className="space-y-2">
      <p className="text-sm text-gray-600">Quick searches:</p>
      <div className="flex flex-wrap gap-2">
        {quickSearchOptions.map((option, index) => (
          <button
            key={index}
            type="button"
            onClick={() => setQuery(option)}
            className="btn-secondary text-sm"
            disabled={loading}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickSearch;
