import React from 'react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';

const QuickSearch = () => {
  const { setQuery, loading } = useSearchFormContext();

  return (
    <div className="space-y-2">
      <p className="text-sm text-gray-600">{TEXTS.search.quickSearchLabel}</p>
      <div className="flex flex-wrap gap-2">
        {TEXTS.quickSearchOptions.map((option, index) => (
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
