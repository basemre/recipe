import React from 'react';

const Input = ({ type = 'text', value, onChange, placeholder, className = '' }) => (
  <input
    type={type}
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    className={`px-3 py-2 border rounded ${className}`}
  />
);

export default Input;  // Changed from Button to Input