import { useState } from 'react';
import { oddsService } from '../services/oddsService';
import { langGraphAgent } from '../services/langGraphAgent';

export const useOddsData = () => {
  const [odds, setOdds] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchOdds = async (searchQuery) => {
    setLoading(true);
    setError(null);
    
    try {
      let processedQuery = searchQuery;

      if (searchQuery.type === 'natural') {
        console.log('Processing natural language query with LangGraph...');
        processedQuery = await langGraphAgent.processQuery(searchQuery.query);
      } else {
        processedQuery = { query: searchQuery.query, matchFound: true };
      }

      if (!processedQuery.matchFound) {
        throw new Error('Could not find a matching Premier League fixture for your query.');
      }

      const oddsData = await oddsService.getOdds(processedQuery.query);
      
      if (!oddsData || oddsData.length === 0) {
        throw new Error('No odds data found for this match. It may not be scheduled or available yet.');
      }

      setOdds(oddsData);
    } catch (err) {
      console.error('Error fetching odds:', err);
      setError(err.message || 'Failed to fetch odds data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearData = () => {
    setOdds(null);
    setError(null);
  };

  return {
    odds,
    loading,
    error,
    fetchOdds,
    clearData
  };
};
