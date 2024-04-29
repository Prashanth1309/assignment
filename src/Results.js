
import React from 'react';

const Results = ({ publications, onSelect, currentPage, totalPages, onPageChange }) => {
  return (
    <div>
      <select onChange={(event) => onSelect(event.target.value)}>
        <option value="">Select a publication</option>
        {publications.map((pub) => (
          <option key={pub} value={pub}>
            {pub}
          </option>
        ))}
      </select>
      <div>
        <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 0}>
          Previous
        </button>
        <span>Page {currentPage + 1} of {totalPages}</span>
        <button onClick={() => onPageChange(currentPage + 1)} disabled={currentPage >= totalPages - 1}>
          Next
        </button>
      </div>
    </div>
  );
};

export default Results;

