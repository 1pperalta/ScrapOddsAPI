import React from 'react';
import { TEXTS } from '../constants/texts';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-500">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center space-x-4">
          <img 
            src="/nexa-icon.png" 
            alt="Nexa Logo" 
            className="w-14 h-14"
          />
          <h1 className="text-3xl font-bold text-dark">
            Nexa
          </h1>
        </div>
      </div>
    </header>
  );
};

export default Header;
