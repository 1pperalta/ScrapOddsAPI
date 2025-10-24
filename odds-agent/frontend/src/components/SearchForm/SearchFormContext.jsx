import { createContext, useContext } from 'react';
import { TEXTS } from '../../constants/texts';

const SearchFormContext = createContext(null);

export const useSearchFormContext = () => {
  const context = useContext(SearchFormContext);
  if (!context) {
    throw new Error(TEXTS.errors.contextError);
  }
  return context;
};

export default SearchFormContext;
