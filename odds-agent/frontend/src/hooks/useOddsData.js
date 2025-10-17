import { useState } from 'react';
import { geminiAgent } from '../services/geminiAgent';
import { TEXTS } from '../constants/texts';

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
        console.log('Processing natural language query with Gemini...');
        processedQuery = await geminiAgent.processQuery(searchQuery.query);
      } else {
        // For direct search, also use the agent
        processedQuery = await geminiAgent.processQuery(searchQuery.query);
      }

      if (!processedQuery.matchFound) {
        throw new Error(TEXTS.errors.noMatchFound);
      }

      // Format the response properly for your components
      setOdds({
        // Wrap the analysis in an array if your component expects to iterate
        matches: [{
          analysis: processedQuery.query,
          analysisType: processedQuery.analysisType,
          confidence: processedQuery.confidence,
          id: 1 // Add an ID if needed
        }],
        // Or keep the original structure and let components handle it
        analysis: processedQuery.query,
        analysisType: processedQuery.analysisType,
        confidence: processedQuery.confidence
      });
      
    } catch (err) {
      console.error('Error fetching odds:', err);
      setError(err.message || TEXTS.errors.fetchFailed);
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