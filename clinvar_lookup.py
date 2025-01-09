#!/usr/bin/env python3
"""
ClinVar API Integration Module
Handles querying ClinVar API with rate limiting and caching.
"""

import requests
import time
import json
from pathlib import Path

class ClinVarLookup:
    """Handles ClinVar API queries with rate limiting and caching."""
    
    def __init__(self, cache_file='clinvar_cache.json'):
        """Initialize ClinVar lookup with caching.
        
        Args:
            cache_file (str): Path to cache file
        """
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.last_call_time = 0  # For rate limiting
        
    def _load_cache(self):
        """Load cached results from file."""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
            
    def _save_cache(self):
        """Save current cache to file."""
        # Ensure directory exists
        Path(self.cache_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
            
    def get_clinical_significance(self, spdi):
        """Query ClinVar API for clinical significance of variant.
        
        Args:
            spdi (str): Variant in SPDI notation
            
        Returns:
            str: Clinical significance or 'Unknown' if not found
        """
        # Check cache first
        if spdi in self.cache:
            return self.cache[spdi]
            
        # Implement rate limiting
        now = time.time()
        if now - self.last_call_time < 1:
            time.sleep(1 - (now - self.last_call_time))
        self.last_call_time = time.time()
        
        # Query API
        try:
            url = f"https://api.ncbi.nlm.nih.gov/variation/v0/spdi/{spdi}/"
            response = requests.get(url, headers={'Accept': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                # Extract clinical significance from response
                significance = (
                    data.get('clinical_significance', {})
                    .get('description', 'Unknown')
                )
                
                # Cache result
                self.cache[spdi] = significance
                self._save_cache()
                return significance
                
            elif response.status_code == 404:
                # Variant not found in ClinVar
                self.cache[spdi] = 'Not found in ClinVar'
                self._save_cache()
                return 'Not found in ClinVar'
                
            else:
                # Other API errors
                print(f"API Error ({response.status_code}): {response.text}")
                return 'API Error'
                
        except Exception as e:
            print(f"Error querying ClinVar API: {str(e)}")
            return 'Error'
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure cache is saved."""
        self._save_cache()
