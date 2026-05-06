"""
Medical Research AI - Main Application Entry Point  
Integrates data from OpenAlex, PubMed, and ClinicalTrials
"""

import os
import sys
from datetime import datetime
#from services.openalexService import OpenAlexService
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import services
from services.openalexService import OpenAlexService
from services.pubmedService import PubMedService
from services.clinicaltrialService import ClinicalTrialService
from services.dataProcessor import DataProcessor
from models.researchAnalyzer import ResearchAnalyzer

# Initialize services
openalexService = OpenAlexService()
pubmedService = PubMedService()
clinicaltrialService = ClinicalTrialService()
dataProcessor = DataProcessor()
analyzer = ResearchAnalyzer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'service': 'Medical Research AI',
        'version': '1.0.0'
    }), 200

@app.route('/api/search/combined', methods=['POST'])
def search_combined():
    """
    Search across all data sources: OpenAlex, PubMed, and ClinicalTrials
    """
    try:
        data = request.get_json()
        query = data.get('query')
        disease = data.get('disease', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        logger.info(f"Searching for: {query} in disease: {disease}")
        
        # Perform searches
        openalex_results = openalexService.search_by_disease(disease, query) if disease else openalexService.search(query)
        pubmed_results = pubmedService.search(query, disease)
        clinicaltrial_results = clinicaltrialService.search(query, disease)
        
        # Process and combine results
        combined_data = {
            'openalex': openalex_results,
            'pubmed': pubmed_results,
            'clinicaltrials': clinicaltrial_results
        }
        
        # Analyze the combined data
        analysis = analyzer.analyze(combined_data)
        
        return jsonify({
            'query': query,
            'results': combined_data,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in search_combined: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_research():
    """
    Analyze research data and provide insights
    """
    try:
        data = request.get_json()
        research_data = data.get('data', {})
        
        analysis_results = analyzer.analyze(research_data)
        
        return jsonify({
            'analysis': analysis_results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_research: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict disease outcomes based on research data
    """
    try:
        data = request.get_json()
        features = data.get('features', {})
        
        prediction = analyzer.predict(features)
        
        return jsonify({
            'prediction': prediction,
            'confidence': analyzer.get_confidence_score(features),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in predict: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_PORT', 5001))
    debug = os.getenv('DEBUG', 'False') == 'True'
    
    logger.info(f"Starting Medical Research AI on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
