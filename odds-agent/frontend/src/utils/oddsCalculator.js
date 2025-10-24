export const calculateBestOdds = (bookmakers) => {
  const outcomeOdds = {};
  
  bookmakers.forEach(bookie => {
    if (!outcomeOdds[bookie.outcome]) {
      outcomeOdds[bookie.outcome] = [];
    }
    outcomeOdds[bookie.outcome].push({
      bookmaker: bookie.name,
      odds: bookie.odds,
      region: bookie.region
    });
  });

  const bestOdds = {};
  Object.keys(outcomeOdds).forEach(outcome => {
    bestOdds[outcome] = outcomeOdds[outcome].reduce((best, current) => 
      current.odds > best.odds ? current : best
    );
  });

  return bestOdds;
};

// Deprecated: Use getOutcomeIcon from iconHelpers.jsx instead
export const getOutcomeEmoji = (outcome, homeTeam, awayTeam) => {
  console.warn('getOutcomeEmoji is deprecated. Use getOutcomeIcon from iconHelpers.jsx instead');
  switch (outcome.toLowerCase()) {
    case homeTeam.toLowerCase():
      return '🏠';
    case awayTeam.toLowerCase():
      return '✈️';
    case 'draw':
      return '🤝';
    default:
      return '⚽';
  }
};

export const calculateImpliedProbability = (odds) => {
  return ((1 / odds) * 100).toFixed(1);
};

export const groupOddsByOutcome = (bookmakers) => {
  const oddsGrouped = {};
  
  bookmakers.forEach(bookie => {
    if (!oddsGrouped[bookie.outcome]) {
      oddsGrouped[bookie.outcome] = [];
    }
    oddsGrouped[bookie.outcome].push(bookie);
  });

  Object.keys(oddsGrouped).forEach(outcome => {
    oddsGrouped[outcome].sort((a, b) => b.odds - a.odds);
  });

  return oddsGrouped;
};
