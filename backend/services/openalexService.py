"""
OpenAlex Service - Python version for fetching academic research data
"""

import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class OpenAlexService:
    """Service to interact with OpenAlex API"""
    
    def __init__(self):
        self.base_url = 'https://api.openalex.org/'
        
    def search(self, query: str) -> Dict:
        """
        Search OpenAlex for works
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing research works
        """
        try:
            params = {
                'search': query,
                'per_page': 20,
                'sort': 'cited_by_count:desc'
            }
            
            response = requests.get(
                f"{self.base_url}works",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            works = []
            
            for work in data.get('results', []):
                processed_work = self._process_work(work)
                works.append(processed_work)
            
            logger.info(f"Found {len(works)} works for query: {query}")
            
            return {
                'source': 'OpenAlex',
                'query': query,
                'total_results': data.get('meta', {}).get('count', 0),
                'works': works
            }
            
        except Exception as e:
            logger.error(f"Error searching OpenAlex: {str(e)}")
            return {
                'source': 'OpenAlex',
                'error': str(e),
                'works': []
            }
    
    def search_by_disease(self, disease: str, query: str) -> Dict:
        """
        Search OpenAlex filtered by disease concept
        
        Args:
            disease: Disease concept name
            query: Additional search query
            
        Returns:
            Dictionary containing filtered research works
        """
        try:
            search_query = f"{query} {disease}"
            params = {
                'search': search_query,
                'per_page': 20,
                'sort': 'cited_by_count:desc'
            }
            
            response = requests.get(
                f"{self.base_url}works",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            works = []
            
            for work in data.get('results', []):
                processed_work = self._process_work(work)
                works.append(processed_work)
            
            logger.info(f"Found {len(works)} works for disease: {disease}, query: {query}")
            
            return {
                'source': 'OpenAlex',
                'disease': disease,
                'query': query,
                'total_results': data.get('meta', {}).get('count', 0),
                'works': works
            }
            
        except Exception as e:
            logger.error(f"Error searching OpenAlex by disease: {str(e)}")
            return {
                'source': 'OpenAlex',
                'error': str(e),
                'works': []
            }
    
    def _process_work(self, work: Dict) -> Dict:
        """
        Process raw work data into structured format
        
        Args:
            work: Raw work data from API
            
        Returns:
            Processed work dictionary
        """
        try:
            authors = []
            for author in work.get('authorships', []):
                author_name = author.get('author', {}).get('display_name', 'Unknown')
                authors.append(author_name)
            
            return {
                'id': work.get('id', 'N/A'),
                'title': work.get('title', 'N/A'),
                'authors': authors,
                'publication_year': work.get('publication_year', 'N/A'),
                'cited_by_count': work.get('cited_by_count', 0),
                'is_open_access': work.get('is_oa', False),
                'concepts': [c.get('display_name', '') for c in work.get('concepts', [])[:5]],
                'journal': work.get('host_venue', {}).get('display_name', 'N/A'),
                'abstract': work.get('abstract', 'N/A')
            }
            
        except Exception as e:
            logger.error(f"Error processing work: {str(e)}")
            return {}
