"""
Clinical Trials Service - Fetches clinical trial data
"""

import requests
import logging
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

class ClinicalTrialService:
    """Service to interact with ClinicalTrials.gov API"""
    
    def __init__(self):
        self.base_url = 'https://clinicaltrials.gov/api/query/'
        
    def search(self, query: str, disease: Optional[str] = None) -> Dict:
        """
        Search ClinicalTrials.gov for trials
        
        Args:
            query: Search query string
            disease: Optional disease filter
            
        Returns:
            Dictionary containing trial results
        """
        try:
            search_query = f"{query} {disease}" if disease else query
            
            params = {
                'expr': search_query,
                'fmt': 'json',
                'pageSize': 20
            }
            
            response = requests.get(
                f"{self.base_url}full_studies",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            trials_data = data.get('NStudiesReturned', 0)
            trials = []
            
            for trial in data.get('NStudiesReturned', {}).get('FullStudiesResponse', {}).get('ListStudies', []):
                processed_trial = self._process_trial(trial)
                if processed_trial:
                    trials.append(processed_trial)
            
            logger.info(f"Found {trials_data} clinical trials for query: {search_query}")
            
            return {
                'source': 'ClinicalTrials.gov',
                'query': query,
                'total_results': trials_data,
                'trials': trials
            }
            
        except Exception as e:
            logger.error(f"Error searching ClinicalTrials: {str(e)}")
            return {
                'source': 'ClinicalTrials.gov',
                'error': str(e),
                'trials': []
            }
    
    def _process_trial(self, trial_data: Dict) -> Optional[Dict]:
        """
        Process raw trial data into structured format
        
        Args:
            trial_data: Raw trial data from API
            
        Returns:
            Processed trial dictionary or None
        """
        try:
            study = trial_data.get('Study', {})
            protocol = study.get('ProtocolSection', {})
            id_section = protocol.get('IdentificationModule', {})
            status = protocol.get('StatusModule', {})
            
            return {
                'nct_id': id_section.get('NCTId', 'N/A'),
                'title': id_section.get('OfficialTitle', 'N/A'),
                'status': status.get('OverallStatus', 'N/A'),
                'phase': protocol.get('DesignModule', {}).get('PhaseList', {}).get('Phase', []),
                'enrollment': status.get('TargetDuration', 'N/A'),
                'sponsor': id_section.get('Organization', {}).get('OrganizationFullName', 'N/A'),
                'start_date': status.get('StartDateStruct', {}).get('StartDate', 'N/A'),
                'conditions': protocol.get('ConditionsModule', {}).get('ConditionList', {}).get('Condition', []),
                'interventions': self._extract_interventions(protocol)
            }
            
        except Exception as e:
            logger.error(f"Error processing trial: {str(e)}")
            return None
    
    def _extract_interventions(self, protocol: Dict) -> List[str]:
        """
        Extract intervention names from protocol
        
        Args:
            protocol: Protocol section data
            
        Returns:
            List of intervention names
        """
        try:
            arms = protocol.get('ArmsInterventionsModule', {}).get('InterventionList', {}).get('Intervention', [])
            interventions = []
            
            if isinstance(arms, dict):
                interventions.append(arms.get('InterventionName', 'N/A'))
            elif isinstance(arms, list):
                for arm in arms:
                    interventions.append(arm.get('InterventionName', 'N/A'))
            
            return interventions
            
        except Exception as e:
            logger.error(f"Error extracting interventions: {str(e)}")
            return []
