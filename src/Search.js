import React, { useState } from 'react';

const Search = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(input);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Search publications..."
      />
      <button type="submit">Search</button>
    </form>
  );
};

export default Search;
