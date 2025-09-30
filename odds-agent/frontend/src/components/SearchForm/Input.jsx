import React from 'react';
import { useSearchFormContext } from './SearchFormContext';

const Input = () => {
  const { query, setQuery, searchType, loading } = useSearchFormContext();

  return (
    <div className="relative">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={
          searchType === 'natural'
            ? "e.g., 'Show me odds for Arsenal vs Chelsea this weekend'"
            : "e.g., 'Arsenal vs Chelsea'"
        }
        className="input-field pr-12"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={!query.trim() || loading}
        className="absolute right-2 top-1/2 transform -translate-y-1/2 btn-primary px-3 py-1 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? '...' : '🔍'}
      </button>
    </div>
  );
};

export default Input;
