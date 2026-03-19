import React, { useState } from 'react';
import { ChartBar } from 'phosphor-react';
import { useProcessedMatches } from '../hooks/useProcessedMatches';
import MatchCard from './MatchCard';
import OddsComparison from './OddsComparison';
import { TEXTS } from '../constants/texts';
import DirectMatchDisplay from './DirectMatchDisplay';

const OddsDisplay = ({ oddsData }) => {
  // Normalize the LLM text but keep markdown markers intact (so we can render them)
  const normalizeAnalysisText = (text) => {
    if (!text) return '';
    return text
      .replace(/\r/g, '')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  };

  // Minimal inline markdown: renders "**bold**" as <strong>
  const renderInline = (text) => {
    const parts = [];
    const regex = /\*\*(.+?)\*\*/g;
    let lastIndex = 0;
    let match;
    let idx = 0;

    // eslint-disable-next-line no-cond-assign
    while ((match = regex.exec(text)) !== null) {
      const start = match.index;
      const end = start + match[0].length;

      if (start > lastIndex) {
        parts.push(<React.Fragment key={`t-${idx++}`}>{text.slice(lastIndex, start)}</React.Fragment>);
      }

      parts.push(
        <strong key={`b-${idx++}`} className="font-semibold">
          {match[1]}
        </strong>
      );

      lastIndex = end;
    }

    if (lastIndex < text.length) {
      parts.push(<React.Fragment key={`t-${idx++}`}>{text.slice(lastIndex)}</React.Fragment>);
    }

    return parts.length ? parts : text;
  };

  // Minimal markdown-like block renderer.
  // Produces a more sorted layout without bringing a full markdown dependency.
  const renderMarkdownish = (text) => {
    const normalized = normalizeAnalysisText(text);
    if (!normalized) return null;

    const lines = normalized.split('\n');
    const nodes = [];
    let i = 0;
    let nodeKey = 0;

    const isHeading = (l) => l.startsWith('## ') || l.startsWith('### ') || l.startsWith('# ');
    const headingLevel = (l) => {
      if (l.startsWith('### ')) return 4;
      if (l.startsWith('# ')) return 3;
      return 3; // "## "
    };

    while (i < lines.length) {
      const line = lines[i].trimEnd();
      const trimmed = line.trim();

      if (!trimmed) {
        i += 1;
        continue;
      }

      if (isHeading(line)) {
        const level = headingLevel(line);
        const titleText = line.replace(/^#{1,3}\s+/, '');
        const HeadingTag = `h${level}`;
        nodes.push(
          <HeadingTag
            key={`n-${nodeKey++}`}
            className={level === 4 ? 'text-base font-bold text-dark mt-3' : 'text-lg font-bold text-dark mt-3'}
          >
            {renderInline(titleText)}
          </HeadingTag>
        );
        i += 1;
        continue;
      }

      const unorderedListMatch = /^[-*]\s+/.test(trimmed);
      if (unorderedListMatch) {
        const items = [];
        while (i < lines.length) {
          const l = lines[i].trim();
          if (!/^[-*]\s+/.test(l)) break;
          items.push(l.replace(/^[-*]\s+/, ''));
          i += 1;
        }
        nodes.push(
          <ul key={`n-${nodeKey++}`} className="list-disc pl-5 text-dark">
            {items.map((it, idx) => (
              <li key={`li-${idx}`} className="mb-1">
                {renderInline(it)}
              </li>
            ))}
          </ul>
        );
        continue;
      }

      const orderedListMatch = /^\d+\.\s+/.test(trimmed);
      if (orderedListMatch) {
        const items = [];
        while (i < lines.length) {
          const l = lines[i].trim();
          if (!/^\d+\.\s+/.test(l)) break;
          items.push(l.replace(/^\d+\.\s+/, ''));
          i += 1;
        }
        nodes.push(
          <ol key={`n-${nodeKey++}`} className="list-decimal pl-5 text-dark">
            {items.map((it, idx) => (
              <li key={`li-${idx}`} className="mb-1">
                {renderInline(it)}
              </li>
            ))}
          </ol>
        );
        continue;
      }

      // Paragraph: consume until a blank line or another block starts
      const paragraphLines = [];
      while (i < lines.length) {
        const l = lines[i];
        const t = l.trim();
        if (!t) break;
        if (isHeading(l)) break;
        if (/^[-*]\s+/.test(t)) break;
        if (/^\d+\.\s+/.test(t)) break;
        paragraphLines.push(t);
        i += 1;
      }

      nodes.push(
        <p key={`n-${nodeKey++}`} className="text-dark leading-relaxed mb-2">
          {renderInline(paragraphLines.join(' '))}
        </p>
      );
    }

    return nodes;
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
                {renderMarkdownish(oddsData.analysis)}
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
        <h3 className="text-lg font-semibold mb-2">Formato de datos inesperado</h3>
        <p>Los datos recibidos no tienen el formato esperado.</p>
      </div>
    </div>
  );
};

export default OddsDisplay;