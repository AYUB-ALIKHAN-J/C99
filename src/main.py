from flask import Flask
from infrastructure.service_repository import ServiceRepositary
from infrastructure.vendor_repository import VendorRepository
from infrastructure.search_indexer import SearchIndexer
from application.catalog_service import CatalogService
from application.search_service import SearchService
from interface.catalog_controller import create_catalog_controller
from interface.search_controller import create_search_controller


app = Flask(__name__)

# --- Infrastructure Layer ---
service_repo = ServiceRepositary()
vendor_repo = VendorRepository()
search_indexer = SearchIndexer()

# --- Application Layer ---
catalog_service = CatalogService(service_repo, vendor_repo)
search_service = SearchService(search_indexer)

# --- Interface Layer (API Controllers) ---
app.register_blueprint(create_catalog_controller(catalog_service))
app.register_blueprint(create_search_controller(search_service))

@app.route("/")
def home():
    return "Service Catalog API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)