import requests
import os
class WebSearcher:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        
    def search(self, query, num_results=10):
        """Perform web search using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': min(num_results, 10)
        }      
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            raise Exception(f"Search API error: {response.status_code}")
        
searcher = WebSearcher(
    api_key="your_api_key_here",
    search_engine_id="your_search_engine_id"
)
results = searcher.search("quantum computing breakthroughs 2025")
