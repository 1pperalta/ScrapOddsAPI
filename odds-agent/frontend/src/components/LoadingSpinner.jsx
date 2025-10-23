import React from 'react';
import { CircleNotch } from 'phosphor-react';

const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center">
      <CircleNotch size={48} weight="bold" className="animate-spin text-premier-600" />
    </div>
  );
};

export default LoadingSpinner;
