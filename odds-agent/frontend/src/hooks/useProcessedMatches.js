import { useState, useMemo } from 'react';

export const useProcessedMatches = (oddsData) => {
  const [sortBy, setSortBy] = useState('date');

  const matches = useMemo(() => {
    if (!oddsData) return [];

    const matchesMap = {};
    oddsData.forEach(odd => {
      const matchKey = `${odd.home}_vs_${odd.away}`;
      if (!matchesMap[matchKey]) {
        matchesMap[matchKey] = {
          home: odd.home,
          away: odd.away,
          kickoff: odd.kickoff,
          bookmakers: []
        };
      }
      matchesMap[matchKey].bookmakers.push({
        name: odd.bookmaker,
        region: odd.region,
        outcome: odd.outcome,
        odds: odd.odds
      });
    });
    return Object.values(matchesMap);
  }, [oddsData]);

  const sortedMatches = useMemo(() => {
    return [...matches].sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(a.kickoff) - new Date(b.kickoff);
        case 'home':
          return a.home.localeCompare(b.home);
        case 'away':
          return a.away.localeCompare(b.away);
        default:
          return 0;
      }
    });
  }, [matches, sortBy]);

  return { sortedMatches, sortBy, setSortBy, matchesCount: matches.length };
};
