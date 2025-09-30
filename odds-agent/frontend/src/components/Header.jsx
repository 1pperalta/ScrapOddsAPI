import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-premier-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">⚽</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Premier League Odds Agent
              </h1>
              <p className="text-gray-600 text-sm">
                AI-powered odds comparison for Premier League matches
              </p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-4 text-sm text-gray-600">
            <span>🤖 Powered by LangGraph</span>
            <span>•</span>
            <span>📊 Real-time odds</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
