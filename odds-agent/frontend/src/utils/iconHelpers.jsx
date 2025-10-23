import React from 'react';
import { House, Airplane, Handshake, SoccerBall } from 'phosphor-react';

export const getOutcomeIcon = (outcome, homeTeam, awayTeam, size = 16, weight = 'fill') => {
  switch (outcome.toLowerCase()) {
    case homeTeam?.toLowerCase():
      return <House size={size} weight={weight} />;
    case awayTeam?.toLowerCase():
      return <Airplane size={size} weight={weight} />;
    case 'draw':
      return <Handshake size={size} weight={weight} />;
    default:
      return <SoccerBall size={size} weight={weight} />;
  }
};
