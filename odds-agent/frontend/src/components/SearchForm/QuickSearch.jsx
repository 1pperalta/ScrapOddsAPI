import React, { useState, useEffect } from 'react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';
import axios from 'axios';

const QuickSearch = () => {
  const { setQuery, loading, query } = useSearchFormContext();
  const [selectedOption, setSelectedOption] = useState(null);
  const [quickMatches, setQuickMatches] = useState(TEXTS.quickSearchOptions);

  // Fetch random upcoming matches on component mount
  useEffect(() => {
    const fetchQuickMatches = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/quick-matches');
        if (response.data.matches && response.data.matches.length > 0) {
          setQuickMatches(response.data.matches);
        }
      } catch (error) {
        console.error('Error fetching quick matches:', error);
        // Keep default matches from TEXTS if API fails
      }
    };

    fetchQuickMatches();
  }, []); // Empty dependency array = fetch only once on mount

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    setQuery(option);
  };

  // Limpiar la selección cuando el query sea diferente al seleccionado
  useEffect(() => {
    if (query === '' || (selectedOption && query !== selectedOption)) {
      setSelectedOption(null);
    }
  }, [query, selectedOption]);

  return (
    <div className="space-y-2">
      <p className="text-sm text-gray-500">{TEXTS.search.quickSearchLabel}</p>
      <div className="flex flex-wrap gap-2">
        {quickMatches.map((option, index) => {
          const isSelected = selectedOption === option;
          return (
            <button
              key={index}
              type="button"
              onClick={() => handleOptionClick(option)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isSelected
                  ? 'bg-premier-500 text-white shadow-md'
                  : 'bg-gray-500 text-white hover:bg-premier-500 hover:text-white'
              }`}
              disabled={loading}
            >
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default QuickSearch;
