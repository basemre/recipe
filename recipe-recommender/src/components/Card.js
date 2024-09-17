import React from 'react';

const Card = ({ children, className = '' }) => (
  <div className={`bg-white shadow rounded-lg p-6 ${className}`}>
    {children}
  </div>
);

export default Card;