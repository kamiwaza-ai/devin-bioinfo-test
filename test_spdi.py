#!/usr/bin/env python3
"""
Test script for NCBI E-utilities ClinVar API.
Tests retrieving clinical significance data for variants.
"""

import requests
import time
import json

def test_clinvar_api():
    """Test ClinVar E-utilities API with a known pathogenic variant."""
    # Test with BRCA1 pathogenic variant (GRCh38)
    chrom = '17'
    pos = '43093268'
    ref = 'G'
    alt = 'A'
    
    # First, search for the variant
    search_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    search_params = {
        'db': 'clinvar',
        'term': f'({chrom}[Chromosome] AND {pos}[Base Position]) AND "GRCh38"[Assembly]',
        'retmode': 'json'
    }
    
    print(f'Searching ClinVar for variant chr{chrom}:{pos}{ref}>{alt}')
    
    try:
        # Search for variant ID
        search_response = requests.get(search_url, params=search_params)
        print(f'Search Status: {search_response.status_code}')
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            print('\nSearch Response:')
            print(json.dumps(search_data, indent=2))
            
            # Get variant details if found
            if 'esearchresult' in search_data and 'idlist' in search_data['esearchresult']:
                variant_ids = search_data['esearchresult']['idlist']
                if variant_ids:
                    # Get details for first matching variant
                    time.sleep(1)  # Respect rate limit
                    summary_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
                    summary_params = {
                        'db': 'clinvar',
                        'id': variant_ids[0],
                        'retmode': 'json'
                    }
                    
                    print(f'\nFetching details for variant ID: {variant_ids[0]}')
                    summary_response = requests.get(summary_url, params=summary_params)
                    print(f'Details Status: {summary_response.status_code}')
                    
                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        print('\nVariant Details:')
                        print(json.dumps(summary_data, indent=2))
                        
                        # Extract clinical significance if available
                        if 'result' in summary_data:
                            result = summary_data['result']
                            variant_id = variant_ids[0]
                            if variant_id in result:
                                variant = result[variant_id]
                                if 'clinical_significance' in variant:
                                    print(f'\nClinical Significance: {variant["clinical_significance"]["description"]}')
                                if 'trait_set' in variant:
                                    print('\nAssociated Conditions:')
                                    for trait in variant['trait_set']:
                                        print(f'- {trait["trait_name"]}')
            else:
                print('\nNo variants found at this position')
        else:
            print(f'Error Response: {search_response.text}')
            
    except Exception as e:
        print(f'Error making request: {str(e)}')

if __name__ == '__main__':
    test_clinvar_api()
