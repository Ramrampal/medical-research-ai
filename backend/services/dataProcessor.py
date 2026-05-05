"""
Data Processor - Processes and normalizes data from multiple sources
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DataProcessor:
    """Service to process and normalize research data"""
    
    def __init__(self):
        self.logger = logger
        
    def process_combined_data(self, data: Dict) -> pd.DataFrame:
        """
        Process data from multiple sources into a unified DataFrame
        
        Args:
            data: Dictionary containing results from multiple sources
            
        Returns:
            Processed pandas DataFrame
        """
        try:
            all_records = []
            
            # Process OpenAlex data
            openalex_data = data.get('openalex', {})
            if openalex_data and 'works' in openalex_data:
                for work in openalex_data['works']:
                    record = {
                        'source': 'OpenAlex',
                        'title': work.get('title', ''),
                        'authors': ','.join(work.get('authors', [])),
                        'year': work.get('publication_year', 0),
                        'cited_count': work.get('cited_by_count', 0),
                        'is_oa': work.get('is_open_access', False),
                        'journal': work.get('journal', ''),
                        'concepts': ','.join(work.get('concepts', []))
                    }
                    all_records.append(record)
            
            # Process PubMed data
            pubmed_data = data.get('pubmed', {})
            if pubmed_data and 'articles' in pubmed_data:
                for article in pubmed_data['articles']:
                    record = {
                        'source': 'PubMed',
                        'title': article.get('title', ''),
                        'authors': ','.join([a.get('name', '') for a in article.get('authors', [])]),
                        'year': self._extract_year(article.get('pub_date', '')),
                        'cited_count': 0,
                        'is_oa': True,
                        'journal': article.get('journal', ''),
                        'concepts': ','.join(article.get('keywords', []))
                    }
                    all_records.append(record)
            
            # Process ClinicalTrials data
            clinicaltrials_data = data.get('clinicaltrials', {})
            if clinicaltrials_data and 'trials' in clinicaltrials_data:
                for trial in clinicaltrials_data['trials']:
                    record = {
                        'source': 'ClinicalTrials.gov',
                        'title': trial.get('title', ''),
                        'authors': trial.get('sponsor', ''),
                        'year': self._extract_year(trial.get('start_date', '')),
                        'cited_count': 0,
                        'is_oa': True,
                        'journal': 'Clinical Trial',
                        'concepts': ','.join(trial.get('conditions', []))
                    }
                    all_records.append(record)
            
            df = pd.DataFrame(all_records)
            logger.info(f"Processed {len(df)} records from multiple sources")
            
            return df
            
        except Exception as e:
            logger.error(f"Error processing combined data: {str(e)}")
            return pd.DataFrame()
    
    def _extract_year(self, date_str: str) -> int:
        """
        Extract year from various date formats
        
        Args:
            date_str: Date string
            
        Returns:
            Year as integer
        """
        try:
            if isinstance(date_str, str) and len(date_str) >= 4:
                return int(date_str[:4])
            return 0
        except:
            return 0
    
    def calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate statistics from processed data
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary with statistics
        """
        try:
            if df.empty:
                return {}
            
            stats = {
                'total_records': len(df),
                'sources_count': df['source'].nunique(),
                'date_range': {
                    'min_year': int(df['year'].min()) if df['year'].min() > 0 else 0,
                    'max_year': int(df['year'].max()) if df['year'].max() > 0 else 0
                },
                'open_access_percentage': (df['is_oa'].sum() / len(df) * 100) if len(df) > 0 else 0,
                'avg_citations': float(df['cited_count'].mean()),
                'most_cited_work': self._get_most_cited(df),
                'sources_breakdown': df['source'].value_counts().to_dict()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {str(e)}")
            return {}
    
    def _get_most_cited(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get most cited work"""
        try:
            most_cited = df.loc[df['cited_count'].idxmax()]
            return {
                'title': most_cited['title'],
                'citations': int(most_cited['cited_count']),
                'source': most_cited['source']
            }
        except:
            return {}
    
    def filter_by_date_range(self, df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Filter dataframe by year range
        
        Args:
            df: Input DataFrame
            start_year: Start year
            end_year: End year
            
        Returns:
            Filtered DataFrame
        """
        return df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    def sort_by_relevance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sort dataframe by relevance (citations + recency)
        
        Args:
            df: Input DataFrame
            
        Returns:
            Sorted DataFrame
        """
        try:
            df['relevance_score'] = (df['cited_count'] * 0.7) + (df['year'] * 0.3)
            return df.sort_values('relevance_score', ascending=False).drop('relevance_score', axis=1)
        except Exception as e:
            logger.error(f"Error sorting by relevance: {str(e)}")
            return df
