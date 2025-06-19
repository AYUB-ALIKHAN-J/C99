import logging
from flask import Flask
from src.infrastructure.service_repository import ServiceRepository
from src.infrastructure.vendor_repository import VendorRepository
from src.infrastructure.search_indexer import SearchIndexer
from src.application.catalog_service import CatalogService
from src.application.search_service import SearchService
from src.application.vendor_service import VendorService
from src.interface.catalog_controller import create_catalog_controller
from src.interface.search_controller import create_search_controller
from src.interface.vendor_controller import create_vendor_controller

# Setup logging for the whole application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

# Initialize Repositories
service_repo = ServiceRepository()
vendor_repo = VendorRepository()
search_indexer = SearchIndexer()

# Initialize Application Services
catalog_service = CatalogService(service_repo, vendor_repo)
search_service = SearchService(search_indexer)
vendor_service = VendorService(vendor_repo)

# Register Blueprints (Controllers)
app.register_blueprint(create_catalog_controller(catalog_service))
app.register_blueprint(create_search_controller(search_service))
app.register_blueprint(create_vendor_controller(vendor_service))

logging.info("Flask app initialized and all blueprints registered.")

if __name__ == "__main__":
    logging.info("Starting Flask app on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
