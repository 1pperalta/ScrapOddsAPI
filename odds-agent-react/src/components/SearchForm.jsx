import React, { useState } from 'react'

const SearchForm = ({ onSearch, loading }) => {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState('natural')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch({ query: query.trim(), type: searchType })
    }
  }

  const quickSearchOptions = [
    'Arsenal vs Chelsea',
    'Manchester United vs Liverpool',
    'Manchester City vs Tottenham',
    'Newcastle vs Brighton'
  ]

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Search Type Toggle */}
      <div className="flex items-center space-x-4">
        <span className="text-sm font-medium text-gray-700">Search mode:</span>
        <div className="flex space-x-2">
          <button
            type="button"
            onClick={() => setSearchType('natural')}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              searchType === 'natural'
                ? 'bg-premier-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            🤖 Natural Language
          </button>
          <button
            type="button"
            onClick={() => setSearchType('direct')}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              searchType === 'direct'
                ? 'bg-premier-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            📝 Direct Match
          </button>
        </div>
      </div>

      {/* Search Input */}
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={
            searchType === 'natural'
              ? "e.g., 'Show me odds for Arsenal vs Chelsea this weekend'"
              : "e.g., 'Arsenal vs Chelsea'"
          }
          className="input-field pr-12"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={!query.trim() || loading}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 btn-primary px-3 py-1 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '...' : '🔍'}
        </button>
      </div>

      {/* Quick Search Buttons */}
      <div className="space-y-2">
        <p className="text-sm text-gray-600">Quick searches:</p>
        <div className="flex flex-wrap gap-2">
          {quickSearchOptions.map((option, index) => (
            <button
              key={index}
              type="button"
              onClick={() => setQuery(option)}
              className="btn-secondary text-sm"
              disabled={loading}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      {/* Help Text */}
      <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-lg">
        {searchType === 'natural' ? (
          <div>
            <strong>💡 Natural Language Tips:</strong>
            <ul className="mt-1 space-y-1 ml-4">
              <li>• "What are the odds for Arsenal vs Chelsea?"</li>
              <li>• "Show me Manchester United's next match odds"</li>
              <li>• "Give me the best odds for Liverpool"</li>
            </ul>
          </div>
        ) : (
          <div>
            <strong>💡 Direct Search Tips:</strong>
            <ul className="mt-1 space-y-1 ml-4">
              <li>• Use format: "Team A vs Team B"</li>
              <li>• Examples: "Arsenal vs Chelsea", "Man City vs Liverpool"</li>
            </ul>
          </div>
        )}
      </div>
    </form>
  )
}

export default SearchForm
