import React, { useState, useEffect } from 'react';
import { Lightbulb, CaretLeft, CaretRight } from 'phosphor-react';
import { useSearchFormContext } from './SearchFormContext';
import { TEXTS } from '../../constants/texts';

const HelpText = () => {
  const { searchType } = useSearchFormContext();
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  // Define tips arrays for each search type
  const naturalTips = [
    TEXTS.search.naturalTip1,
    TEXTS.search.naturalTip2,
    TEXTS.search.naturalTip3,
    TEXTS.search.naturalTip4,
    TEXTS.search.naturalTip5,
    TEXTS.search.naturalTip6,
    TEXTS.search.naturalTip7,
    TEXTS.search.naturalTip8,
  ];

  const directTips = [
    TEXTS.search.directTip1,
    TEXTS.search.directTip2,
    TEXTS.search.directTip3,
    TEXTS.search.directTip4,
    TEXTS.search.directTip5,
  ];

  const currentTips = searchType === 'natural' ? naturalTips : directTips;

  // Auto-advance carousel every 4 seconds
  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setCurrentTipIndex((prevIndex) => (prevIndex + 1) % currentTips.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [isAutoPlaying, currentTips.length]);

  // Reset index when search type changes
  useEffect(() => {
    setCurrentTipIndex(0);
  }, [searchType]);

  const handlePrevious = () => {
    setIsAutoPlaying(false);
    setCurrentTipIndex((prevIndex) => 
      prevIndex === 0 ? currentTips.length - 1 : prevIndex - 1
    );
  };

  const handleNext = () => {
    setIsAutoPlaying(false);
    setCurrentTipIndex((prevIndex) => (prevIndex + 1) % currentTips.length);
  };

  const handleDotClick = (index) => {
    setIsAutoPlaying(false);
    setCurrentTipIndex(index);
  };

  return (
    <div className="text-sm text-gray-600 bg-gray-50 p-4 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <strong className="flex items-center gap-2 text-dark">
          <Lightbulb size={18} weight="fill" className="text-yellow-500" />
          {searchType === 'natural' ? TEXTS.search.naturalTipsTitle : TEXTS.search.directTipsTitle}
        </strong>
        
        {/* Navigation arrows */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handlePrevious}
            className="p-1 rounded-full hover:bg-gray-200 transition-colors text-dark"
            aria-label="Consejo anterior"
          >
            <CaretLeft size={18} weight="bold" />
          </button>
          <button
            type="button"
            onClick={handleNext}
            className="p-1 rounded-full hover:bg-gray-200 transition-colors text-dark"
            aria-label="Siguiente consejo"
          >
            <CaretRight size={18} weight="bold" />
          </button>
        </div>
      </div>

      {/* Carousel content */}
      <div className="relative overflow-hidden">
        <div 
          className="transition-all duration-500 ease-in-out"
          style={{ 
            transform: `translateX(-${currentTipIndex * 100}%)`,
            display: 'flex'
          }}
        >
          {currentTips.map((tip, index) => (
            <div
              key={index}
              className="min-w-full px-2"
              style={{ flex: '0 0 100%' }}
            >
              <p className="text-base text-dark leading-relaxed">
                {tip}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Indicator dots */}
      <div className="flex justify-center gap-2 mt-3">
        {currentTips.map((_, index) => (
          <button
            key={index}
            type="button"
            onClick={() => handleDotClick(index)}
            className={`h-2 rounded-full transition-all duration-300 ${
              index === currentTipIndex 
                ? 'w-6 bg-premier-500' 
                : 'w-2 bg-gray-300 hover:bg-gray-400'
            }`}
            aria-label={`Ir al consejo ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
};

export default HelpText;