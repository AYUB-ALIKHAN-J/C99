import os
from pymongo import MongoClient
from typing import Any, Dict, List, Optional
from src.domain.service.vendor import Vendor
from src.domain.service.value_objects import Contact, Rating, MediaReference
from bson.objectid import ObjectId # Import ObjectId for type checking/conversion
import uuid
from datetime import datetime, UTC
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class VendorRepository:
    def __init__(self, mongo_url=None, db_name=None):
        mongo_url = mongo_url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("MONGO_DB_NAME", "service_catalog")
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db.vendors
        logging.info("VendorRepository initialized with DB: %s", db_name)

    def _doc_to_vendor(self, doc: Dict[str, Any]) -> Optional[Vendor]:
        """Converts a MongoDB document (dict) to a Vendor dataclass instance."""
        if not doc:
            return None
        
        # Convert nested dictionaries back to dataclass instances
        if 'contact' in doc and isinstance(doc['contact'], dict):
            doc['contact'] = Contact(**doc['contact'])
        if 'rating' in doc and isinstance(doc['rating'], dict):
            doc['rating'] = Rating(**doc['rating'])
        if 'logo' in doc and isinstance(doc['logo'], dict):
            doc['logo'] = MediaReference(**doc['logo'])
        if 'cover_image' in doc and isinstance(doc['cover_image'], dict):
            doc['cover_image'] = MediaReference(**doc['cover_image'])

        if '_id' in doc: # Remove or handle MongoDB's internal _id
            del doc['_id']

        # Convert 'created_at' and 'updated_at' strings back to datetime objects if needed
        if isinstance(doc.get('created_at'), str):
            doc['created_at'] = datetime.fromisoformat(doc['created_at'])
        if isinstance(doc.get('updated_at'), str):
            doc['updated_at'] = datetime.fromisoformat(doc['updated_at'])

        try:
            return Vendor(**doc)
        except TypeError as e:
            logging.error("Error converting document to Vendor: %s - Document: %s", e, doc)
            return None

    def _vendor_to_doc(self, vendor: Vendor) -> Dict[str, Any]:
        """Converts a Vendor dataclass instance to a dictionary suitable for MongoDB storage."""
        return vendor.to_dict() # Use the to_dict method defined in the dataclass

    def get_all_vendors(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        query = filters or {}
        query["is_deleted"] = False
        return list(self.collection.find(query)) # Returns raw dicts

    def get_vendor_by_id(self, vendor_id: str) -> Optional[Dict]:
        """Returns raw MongoDB document for controller to convert."""
        return self.collection.find_one({"id": vendor_id, "is_deleted": False})

    def create_vendor(self, vendor_data: Dict[str, Any]) -> Dict:
        # Ensure system-managed fields are set
        now = datetime.now(UTC).isoformat()
        if 'id' not in vendor_data or not vendor_data['id']:
            vendor_data['id'] = str(uuid.uuid4())
        if 'created_at' not in vendor_data:
            vendor_data['created_at'] = now
        if 'updated_at' not in vendor_data:
            vendor_data['updated_at'] = now
        if 'is_deleted' not in vendor_data:
            vendor_data['is_deleted'] = False
        if 'status' not in vendor_data:
            vendor_data['status'] = 'active'
        # Assuming vendor_data already contains the 'id' and other fields needed for Vendor creation
        self.collection.insert_one(vendor_data)
        logging.info("Vendor created: %s", vendor_data['id'])
        return vendor_data # Return the inserted data as raw dict

    def update_vendor(self, vendor_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        update_data['updated_at'] = datetime.now(UTC).isoformat()
        self.collection.update_one({"id": vendor_id}, {"$set": update_data})
        logging.info("Vendor updated: %s", vendor_id)
        return self.get_vendor_by_id(vendor_id) # Returns raw dict

    def soft_delete_vendor(self, vendor_id: str) -> None:
        self.collection.update_one({"id": vendor_id}, {"$set": {"is_deleted": True}})
        logging.info("Vendor soft-deleted: %s", vendor_id)
