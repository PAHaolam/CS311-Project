import React from 'react';

const Button = ({ handleClick }) => {
  return (
    <button onClick={handleClick}>
      Open Modal
    </button>
  );
};

export default Button;
