import React from 'react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';

const HelpText = () => {
  const { searchType } = useSearchFormContext();

  return (
    <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-lg">
      {searchType === 'natural' ? (
        <div>
          <strong>💡 {TEXTS.search.naturalTipsTitle}</strong>
          <ul className="mt-1 space-y-1 ml-4">
            <li>• {TEXTS.search.naturalTip1}</li>
            <li>• {TEXTS.search.naturalTip2}</li>
            <li>• {TEXTS.search.naturalTip3}</li>
          </ul>
        </div>
      ) : (
        <div>
          <strong>💡 {TEXTS.search.directTipsTitle}</strong>
          <ul className="mt-1 space-y-1 ml-4">
            <li>• {TEXTS.search.directTip1}</li>
            <li>• {TEXTS.search.directTip2}</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default HelpText;
