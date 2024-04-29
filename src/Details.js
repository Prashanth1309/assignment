import React from 'react';

const Details = ({ publication }) => {
  return (
    <div>
      <p>PMID: {publication?.PMID}</p>
      <p>Title: {publication?.Title}</p>
      <p>Publication Year: {publication?.['Publication Year']}</p>    
    </div>
  );
};

export default Details;
