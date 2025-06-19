from typing import Dict, Any, List

class SearchService:
    def __init__(self, search_indexer):
        self.search_indexer = search_indexer

    def search(self, query: str) -> List[Dict]:
        """Performs a search operation using the search indexer."""
        return self.search_indexer.search_services(query)
