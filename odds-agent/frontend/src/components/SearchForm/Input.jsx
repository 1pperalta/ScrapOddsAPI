import React from 'react';
import { MagnifyingGlass } from 'phosphor-react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';

const Input = () => {
  const { query, setQuery, searchType, loading } = useSearchFormContext();

  return (
    <div className="relative flex items-center">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={
          searchType === 'natural'
            ? TEXTS.search.placeholderNatural
            : TEXTS.search.placeholderDirect
        }
        className="input-field pr-16"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={!query.trim() || loading}
        className="absolute right-1 top-1 bottom-1 bg-premier-500 hover:bg-premier-500 text-white font-medium px-4 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {loading ? '...' : <MagnifyingGlass size={20} weight="bold" />}
      </button>
    </div>
  );
};

export default Input;
