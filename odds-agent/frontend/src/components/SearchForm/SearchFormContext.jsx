import { createContext, useContext } from 'react';

const SearchFormContext = createContext(null);

export const useSearchFormContext = () => {
  const context = useContext(SearchFormContext);
  if (!context) {
    throw new Error('SearchForm compound components must be used within SearchForm');
  }
  return context;
};

export default SearchFormContext;
