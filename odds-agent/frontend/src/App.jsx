import React from 'react';
import Header from './components/Header';
import SearchForm from './components/SearchForm/index';
import OddsDisplay from './components/OddsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { useOddsData } from './hooks/useOddsData';
import { TEXTS } from './constants/texts';

const App = () => {
  const { odds, loading, error, fetchOdds } = useOddsData();

  return (
    <div className="min-h-screen bg-gradient-to-br from-premier-50 to-blue-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-500 mb-6">
              {TEXTS.search.title}
            </h2>
            <SearchForm onSearch={fetchOdds} loading={loading}>
              <SearchForm.ModeToggle />
              <SearchForm.Input />
              <SearchForm.QuickSearch />
              <SearchForm.HelpText />
            </SearchForm>
          </div>

          {loading && (
            <div className="card text-center">
              <LoadingSpinner />
              <p className="text-gray-500 mt-4">{TEXTS.loading.fetchingOdds}</p>
            </div>
          )}

          {error && (
            <div className="card bg-red-50 border-red-500">
              <div className="text-red-500">
                <h3 className="font-semibold mb-2">{TEXTS.error.title}</h3>
                <p>{error}</p>
              </div>
            </div>
          )}

          {odds && !loading && (
            <OddsDisplay oddsData={odds} />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
