
import React, { useState } from 'react';
import axios from 'axios';
import Search from './Search';
import Results from './Results';
import Details from './Details';

function App() {
  const [query, setQuery] = useState('');
  const [publications, setPublications] = useState([]);
  const [selectedPublication, setSelectedPublication] = useState(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const searchPublications = async (newQuery, page = 0) => {
    if (newQuery !== query) setCurrentPage(0);
    setQuery(newQuery);

    try {
      const response = await axios.post('http://localhost:5000/publications', {
        query: newQuery,
        restart: page,
        retmax: 10, 
      });
      
      setPublications(response?.data?.esearchresult?.idlist || []);
      setTotalPages(Math.ceil(response.data.count / 10)); 
      setSelectedPublication(null); 
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const fetchDetails = async (id) => {
    try {
      const response = await axios.get(`http://localhost:5000/publications/details?ids=${id}&fields=PMID&fields=Title&fields=Publication%20Year`);
      setSelectedPublication(response.data[0]);
    } catch (error) {
      console.error('Fetch details failed:', error);
    }
  };

  return (
    <div className="App">
      <Search onSubmit={searchPublications} />
      
      {publications.length > 0 &&
        <Results
          publications={publications}
          onSelect={fetchDetails}
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      }
      {selectedPublication && <Details publication={selectedPublication} />}
    </div>
  );
}

export default App;

