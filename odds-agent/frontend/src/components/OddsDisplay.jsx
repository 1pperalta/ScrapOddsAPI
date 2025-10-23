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
          <div className="flex flex-col gap-4">
            <div>
              <h2 className="text-xl font-bold text-dark mb-2 flex items-center gap-2">
                <ChartBar size={24} weight="duotone" className="text-premier-600" />
                {oddsData.analysisType === 'match_analysis' ? 'Análisis de Partido' : 
                 oddsData.analysisType === 'team_analysis' ? 'Análisis de Equipo' :
                 oddsData.analysisType === 'value_bets' ? 'Oportunidades de Valor' :
                 'Análisis de IA'}
              </h2>
              {oddsData.confidence && (
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-sm text-gray-600">Confianza:</span>
                  <div className="flex items-center gap-1">
                    <div className="w-20 h-2 bg-gray-200 rounded-full">
                      <div 
                        className="h-full bg-green-500 rounded-full transition-all duration-300"
                        style={{ width: `${(oddsData.confidence * 100)}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600">
                      {Math.round(oddsData.confidence * 100)}%
                    </span>
                  </div>
                </div>
              )}
            </div>
            
            <div className="prose max-w-none space-y-4">
              {textSections.map((section, index) => {
                const isMatch = section.startsWith('🏆');
                const isTitle = !isMatch && isTitleSection(section);
                
                if (isMatch) {
                  return (
                    <div key={index} className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-4 border-l-4 border-green-500 shadow-sm">
                      <div className="whitespace-pre-wrap text-dark leading-relaxed text-sm">
                        {section}
                      </div>
                    </div>
                  );
                } else if (isTitle) {
                  return (
                    <div key={index} className="my-6">
                      <h3 className="text-lg font-bold text-dark border-b-2 border-blue-500 pb-2 mb-3">
                        {section.trim()}
                      </h3>
                    </div>
                  );
                } else {
                  return (
                    <div key={index} className="my-4">
                      <div className="text-dark leading-relaxed whitespace-pre-wrap">
                        {section.trim()}
                      </div>
                    </div>
                  );
                }
              })}
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
      <div className="text-yellow-600">
        <h3 className="text-lg font-semibold mb-2">⚠️ Formato de datos inesperado</h3>
        <p>Los datos recibidos no tienen el formato esperado.</p>
      </div>
    </div>
  );
};

export default OddsDisplay;