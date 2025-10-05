import React, { useState } from 'react';
import SearchFormContext from './SearchFormContext';
import ModeToggle from './ModeToggle';
import Input from './Input';
import QuickSearch from './QuickSearch';
import HelpText from './HelpText';

const SearchForm = ({ onSearch, loading, children }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('natural');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch({ query: query.trim(), type: searchType });
    }
  };

  const contextValue = {
    query,
    setQuery,
    searchType,
    setSearchType,
    loading
  };

  return (
    <SearchFormContext.Provider value={contextValue}>
      <form onSubmit={handleSubmit} className="space-y-6">
        {children}
      </form>
    </SearchFormContext.Provider>
  );
};

SearchForm.ModeToggle = ModeToggle;
SearchForm.Input = Input;
SearchForm.QuickSearch = QuickSearch;
SearchForm.HelpText = HelpText;

export default SearchForm;
