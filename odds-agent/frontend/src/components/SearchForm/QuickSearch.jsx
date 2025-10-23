import React, { useState, useEffect } from 'react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';

const QuickSearch = () => {
  const { setQuery, loading, query } = useSearchFormContext();
  const [selectedOption, setSelectedOption] = useState(null);

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
      <p className="text-sm text-gray-600">{TEXTS.search.quickSearchLabel}</p>
      <div className="flex flex-wrap gap-2">
        {TEXTS.quickSearchOptions.map((option, index) => {
          const isSelected = selectedOption === option;
          return (
            <button
              key={index}
              type="button"
              onClick={() => handleOptionClick(option)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isSelected
                  ? 'bg-premier-500 text-white shadow-md'
                  : 'bg-gray-200 text-dark hover:bg-premier-500 hover:text-white'
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
