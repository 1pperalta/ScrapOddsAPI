import React, { useState } from 'react';
import { ChartBar } from 'phosphor-react';
import { useProcessedMatches } from '../hooks/useProcessedMatches';
import MatchCard from './MatchCard';
import OddsComparison from './OddsComparison';
import { TEXTS } from '../constants/texts';
import DirectMatchDisplay from './DirectMatchDisplay';

const OddsDisplay = ({ oddsData }) => {
  // Function to format the analysis text
  const formatAnalysisText = (text) => {
    if (!text) return '';
    
    return text
      // Remove excessive asterisks and hashes
      .replace(/\*{2,}/g, '') // Remove ** and ***
      .replace(/#{1,}/g, '') // Remove # ## ###
      .replace(/---/g, '') // Remove separator lines
      
      // Clean up spacing
      .replace(/\n{3,}/g, '\n\n') // Replace multiple newlines with double
      .replace(/^\s+/gm, '') // Remove leading spaces from lines
      
      // Format specific patterns
      .replace(/^(\d+\.\s*)/gm, '🏆 ') // Replace "1. " with trophy emoji
      .replace(/Fecha:/g, '📅 Fecha:')
      .replace(/Cuota:/g, '💰 Cuota:')
      .replace(/Promedio mercado:/g, '📊 Promedio mercado:')
      .replace(/Valor:/g, '💎 Valor:')
      .replace(/Razón:/g, '📝 Razón:')
      
      // Clean up team names and match info
      .replace(/(.+?)\s+Gana\*{0,}/g, '⚽ $1 Gana')
      .replace(/vs\s+/g, ' 🆚 ')
      
      .trim();
  };

  // Function to split text into sections for better display
  const formatTextSections = (text) => {
    const formattedText = formatAnalysisText(text);
    const sections = formattedText.split(/(?=🏆|\n\n(?=\d+\.))/);
    
    return sections.filter(section => section.trim().length > 0);
  };

  // Function to detect if a section is a title/subtitle
  const isTitleSection = (text) => {
    const titlePatterns = [
      /^(Análisis|Analysis|Oportunidades|Opportunities|Recomendaciones|Recommendations)/i,
      /^(Top \d+)/i,
      /^\w+.*:$/m, // Lines ending with colon
      /^[A-Z\s]{5,}$/m // All caps titles
    ];
    return titlePatterns.some(pattern => pattern.test(text.trim()));
  };

  // Handle the new Gemini agent data structure
  if (!oddsData) {
    return (
      <div className="card text-center">
        <div className="text-gray-500">
          <h3 className="text-lg font-semibold mb-2">{TEXTS.oddsDisplay.noMatchesFound}</h3>
          <p>{TEXTS.oddsDisplay.tryDifferentSearch}</p>
        </div>
      </div>
    );
  }

  // Check if we have analysis from Gemini agent
  if (oddsData.analysis) {
    const textSections = formatTextSections(oddsData.analysis);
    
    return (
      <div className="space-y-6">
        <div className="card">
          <div className="flex flex-col h-full">
            <div className="mb-4">
              <h2 className="text-xl font-bold text-dark flex items-center gap-2">
                <ChartBar size={24} weight="duotone" className="text-premier-500" />
                {oddsData.analysisType === 'match_analysis' ? 'Análisis de Partido' : 
                 oddsData.analysisType === 'team_analysis' ? 'Análisis de Equipo' :
                 oddsData.analysisType === 'value_bets' ? 'Oportunidades de Valor' :
                 'Análisis de IA'}
              </h2>
            </div>
            
            {/* Contenedor con scroll y altura máxima */}
            <div className="max-h-[600px] overflow-y-auto p-6 bg-gray-50 rounded-lg border border-gray-200">
              <div className="space-y-4 text-dark text-base leading-relaxed font-sans">
                {textSections.map((section, index) => (
                  <div key={index} className="text-dark text-base leading-relaxed font-sans">
                    {section.trim()}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // New: Handle direct match data type
  if (oddsData && oddsData.type === 'direct_match' && oddsData.found) {
    return <DirectMatchDisplay matchData={oddsData.matchData} />;
  }

  // Fallback: if we somehow get old-style match data, handle it
  if (Array.isArray(oddsData) && oddsData.length === 0) {
    return (
      <div className="card text-center">
        <div className="text-gray-500">
          <h3 className="text-lg font-semibold mb-2">{TEXTS.oddsDisplay.noMatchesFound}</h3>
          <p>{TEXTS.oddsDisplay.tryDifferentSearch}</p>
        </div>
      </div>
    );
  }

  // If we get here, something unexpected happened
  return (
    <div className="card text-center">
      <div className="text-yellow-500">
        <h3 className="text-lg font-semibold mb-2">⚠️ Formato de datos inesperado</h3>
        <p>Los datos recibidos no tienen el formato esperado.</p>
      </div>
    </div>
  );
};

export default OddsDisplay;