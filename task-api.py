"""
This code defines two endpoints:

1. /publications (POST method): Accepts a JSON object with a query and pagination parameters (retstart and retmax).
   It returns a JSON object containing a list of publication IDs based on the query.

2. /publications/details (GET method): Accepts query parameters ids (list of publication IDs) and fields (list of fields to return).
   It returns detailed information for the provided IDs, filtered based on the requested fields.


You can run this Flask server locally by executing this file as python task-api.py.
Then, you can make requests to
        http://localhost:5000/publications
        and
        http://localhost:5000/publications/details
as described in the task.

"""
from flask_cors import CORS
from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)
# Function to retrieve publication IDs based on a query
def get_publication_ids(query, retstart=0, retmax=10):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retstart={retstart}&retmax={retmax}&retmode=json"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch detailed information for a list of IDs
def get_publication_details(pub_ids):
    id_str = ','.join(pub_ids)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_str}&retmode=xml"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    publications = []
    for article in root.findall('.//PubmedArticle'):
        publication = {}
        publication['PMID'] = article.find('.//PMID').text
        publication['Title'] = article.find('.//ArticleTitle').text
        abstract_elem = article.find('.//AbstractText')
        publication['Abstract'] = abstract_elem.text if abstract_elem is not None else ""
        author_list = []
        for author in article.findall('.//Author'):
            lastname = author.find('LastName').text
            firstname = author.find('ForeName').text if author.find('ForeName') is not None else ""
            author_list.append(f"{firstname} {lastname}")
        publication['Author List'] = author_list
        journal_elem = article.find('.//Journal/Title')
        publication['Journal'] = journal_elem.text if journal_elem is not None else ""
        pub_date_elem = article.find('.//JournalIssue/PubDate/Year')
        publication['Publication Year'] = pub_date_elem.text if pub_date_elem is not None else ""
        mesh_terms = [mesh.text for mesh in article.findall('.//MeshHeading/DescriptorName')]
        publication['MeSH Terms'] = mesh_terms
        publications.append(publication)
    return publications

# POST endpoint to retrieve publication IDs based on a query
@app.route('/publications', methods=['POST'])
def search_publications():
    data = request.json
    print(data)
    query = data.get('query',0)
    retstart = data.get('retstart', 1)
    retmax = data.get('retmax', 2)
    pub_ids = get_publication_ids(query, retstart, retmax)
    return jsonify(pub_ids)

# GET endpoint to fetch detailed information for a list of IDs
@app.route('/publications/details', methods=['GET'])
def get_publication_details_route():
    pub_ids = request.args.getlist('ids')
    print(pub_ids)
    fields = request.args.getlist('fields')
    print(fields)
    publications = get_publication_details(pub_ids)
    print(publications)
    filtered_publications = []
    for publication in publications:
        filtered_publication = {key: publication[key] for key in fields if key in publication}
        filtered_publications.append(filtered_publication)
    return jsonify(filtered_publications)

if __name__ == '__main__':
    app.run(debug=True)
