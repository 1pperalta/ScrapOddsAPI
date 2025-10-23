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
      let result;

      if (searchQuery.type === 'direct') {
        // Handle direct search differently
        console.log('Processing direct search...');
        
        // Extract team names from the query
        const teams = searchQuery.query.split(' vs ');
        if (teams.length === 2) {
          result = await geminiAgent.getDirectMatchData(teams[0].trim(), teams[1].trim());
          
          if (result.found) {
            // Set odds data in a format for displaying match details
            setOdds({
              type: 'direct_match',
              matchData: result.matchData,
              found: true
            });
          } else {
            throw new Error(result.message);
          }
        } else {
          throw new Error('Formato incorrecto. Use: "Equipo A vs Equipo B"');
        }
      } else {
        // Handle natural language search as before
        console.log('Processing natural language query with Gemini...');
        result = await geminiAgent.processQuery(searchQuery.query);
        
        if (!result.matchFound) {
          throw new Error(TEXTS.errors.noMatchFound);
        }

        setOdds({
          type: 'analysis',
          analysis: result.query,
          analysisType: result.analysisType,
          confidence: result.confidence
        });
      }
      
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