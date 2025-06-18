class SearchService:
    def __init__(self, search_indexer):
        self.search_indexer = search_indexer

    def search(self, query):
        return self.search_indexer.search_services(query)
