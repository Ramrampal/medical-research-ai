"""
PubMed Service - Fetches medical research articles from PubMed
"""

import requests
import logging
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PubMedService:
    """Service to interact with PubMed API"""
    
    def __init__(self):
        self.base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.search_endpoint = 'esearch.fcgi'
        self.fetch_endpoint = 'efetch.fcgi'
        
    def search(self, query: str, disease: Optional[str] = None) -> Dict:
        """
        Search PubMed for articles
        
        Args:
            query: Search query string
            disease: Optional disease filter
            
        Returns:
            Dictionary containing search results
        """
        try:
            search_query = f"{query} {disease}" if disease else query
            
            params = {
                'db': 'pubmed',
                'term': search_query,
                'retmax': 20,
                'retmode': 'json',
                'tool': 'medical-research-ai',
                'email': 'research@example.com'
            }
            
            response = requests.get(
                f"{self.base_url}{self.search_endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            pmids = data.get('esearchresult', {}).get('idlist', [])
            
            logger.info(f"Found {len(pmids)} articles for query: {search_query}")
            
            # Fetch details for each PMID
            articles = []
            for pmid in pmids[:10]:  # Limit to 10 for performance
                article = self._fetch_article_details(pmid)
                if article:
                    articles.append(article)
            
            return {
                'source': 'PubMed',
                'query': query,
                'total_results': len(data.get('esearchresult', {}).get('idlist', [])),
                'articles': articles
            }
            
        except Exception as e:
            logger.error(f"Error searching PubMed: {str(e)}")
            return {
                'source': 'PubMed',
                'error': str(e),
                'articles': []
            }
    
    def _fetch_article_details(self, pmid: str) -> Optional[Dict]:
        """
        Fetch detailed information for a specific article
        
        Args:
            pmid: PubMed ID
            
        Returns:
            Dictionary with article details or None
        """
        try:
            params = {
                'db': 'pubmed',
                'id': pmid,
                'retmode': 'json',
                'tool': 'medical-research-ai',
                'email': 'research@example.com'
            }
            
            response = requests.get(
                f"{self.base_url}{self.fetch_endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            article = data.get('result', {}).get(pmid, {})
            
            return {
                'pmid': pmid,
                'title': article.get('title', 'N/A'),
                'authors': article.get('authors', []),
                'pub_date': article.get('pubdate', 'N/A'),
                'abstract': article.get('abstract', 'N/A'),
                'journal': article.get('fulljournalname', 'N/A'),
                'keywords': article.get('keywords', [])
            }
            
        except Exception as e:
            logger.error(f"Error fetching article {pmid}: {str(e)}")
            return None
