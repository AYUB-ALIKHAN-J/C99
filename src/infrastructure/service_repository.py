import os
from pymongo import MongoClient, errors
from typing import Any, Dict, List, Optional
from src.domain.service.service import Service
from src.domain.service.value_objects import PricingTier, ServiceAttribute, MediaReference, PricingRule, AvailabilityRule
from bson.objectid import ObjectId
from datetime import datetime, UTC
import uuid
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class ServiceRepository:
    def __init__(self, mongo_url=None, db_name=None):
        mongo_url = mongo_url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("MONGO_DB_NAME", "service_catalog")
        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client[db_name]
            self.collection = self.db.services
            logging.info("ServiceRepository initialized with DB: %s", db_name)
        except errors.PyMongoError as e:
            logging.error("Failed to connect to MongoDB: %s", e)
            raise

    def _doc_to_service(self, doc: Dict[str, Any]) -> Optional[Service]:
        """Converts a MongoDB document (dict) to a Service dataclass instance."""
        if not doc:
            return None
        try:
            # Convert nested dictionaries back to dataclass instances if they exist
            doc['pricing_tiers'] = [PricingTier(**p) for p in doc.get('pricing_tiers', [])]
            doc['attributes'] = [ServiceAttribute(**a) for a in doc.get('attributes', [])]
            doc['images'] = [MediaReference(**i) for i in doc.get('images', [])]
            doc['videos'] = [MediaReference(**v) for v in doc.get('videos', [])]
            doc['pricing_rules'] = [PricingRule(**p) for p in doc.get('pricing_rules', [])]
            doc['availability_rules'] = [AvailabilityRule(**a) for a in doc.get('availability_rules', [])]
            
            # MongoDB's _id is internal, we use the 'id' field of the Service dataclass
            # Ensure 'id' field is used for dataclass instantiation
            if '_id' in doc: # Remove or handle MongoDB's internal _id if it clashes with your 'id' field
                del doc['_id'] # We rely on our 'id' field for uniqueness, not MongoDB's _id for logic

            # Convert 'created_at' and 'updated_at' strings back to datetime objects if needed
            if isinstance(doc.get('created_at'), str):
                doc['created_at'] = datetime.fromisoformat(doc['created_at'])
            if isinstance(doc.get('updated_at'), str):
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'])

            return Service(**doc)
        except Exception as e:
            logging.error("Error converting document to Service: %s - Document: %s", e, doc)
            return None

    def _service_to_doc(self, service: Service) -> Dict[str, Any]:
        """Converts a Service dataclass instance to a dictionary suitable for MongoDB storage."""
        try:
            return service.to_dict() # Use the to_dict method defined in the dataclass
        except Exception as e:
            logging.error("Error converting Service to dict: %s - Service: %s", e, service)
            return {}

    def get_all_services(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 20, sort: Optional[List[tuple]] = None) -> List[Dict]:
        query = filters or {}
        query["is_deleted"] = False
        try:
            cursor = self.collection.find(query).skip(skip).limit(limit)
            if sort:
                cursor = cursor.sort(sort)
            
            # Return as raw dictionaries for controller to convert using utils.py for JSON serialization
            return list(cursor) 
        except errors.PyMongoError as e:
            logging.error("Error fetching all services: %s", e)
            return []

    def get_service_by_id(self, service_id: str) -> Optional[Dict]:
        """Returns raw MongoDB document for controller to convert."""
        try:
            return self.collection.find_one({"id": service_id, "is_deleted": False})
        except errors.PyMongoError as e:
            logging.error("Error fetching service by id %s: %s", service_id, e)
            return None

    def filter_services(self, filters: Dict[str, Any]) -> List[Dict]:
        query = {"is_deleted": False}
        
        # Advanced filtering logic
        if "category" in filters:
            query["category"] = filters["category"]
        if "vendor_id" in filters:
            query["vendor_id"] = filters["vendor_id"]
        if "min_price" in filters or "max_price" in filters:
            price_query = {}
            if "min_price" in filters:
                price_query["$gte"] = filters["min_price"]
            if "max_price" in filters:
                price_query["$lte"] = filters["max_price"]
            query["base_price"] = price_query
        if "tags" in filters:
            query["tags"] = {"$in": filters["tags"]}
        
        # Return as raw dictionaries for controller to convert
        try:
            return list(self.collection.find(query))
        except errors.PyMongoError as e:
            logging.error("Error filtering services: %s", e)
            return []

    def create_service(self, service_data: Dict[str, Any]) -> Dict:
        # Ensure system-managed fields are set
        now = datetime.now(UTC).isoformat()
        if 'id' not in service_data or not service_data['id']:
            service_data['id'] = str(uuid.uuid4())
        if 'created_at' not in service_data:
            service_data['created_at'] = now
        if 'updated_at' not in service_data:
            service_data['updated_at'] = now
        if 'is_deleted' not in service_data:
            service_data['is_deleted'] = False
        if 'status' not in service_data:
            service_data['status'] = 'active'

        # Assuming service_data already contains the 'id' and other fields needed for Service creation
        # You might want to validate service_data against your Service dataclass structure here
        try:
            self.collection.insert_one(service_data)
            logging.info("Service created: %s", service_data['id'])
            return service_data # Return the inserted data as raw dict
        except errors.PyMongoError as e:
            logging.error("Error creating service: %s - Data: %s", e, service_data)
            return {}

    def update_service(self, service_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        update_data['updated_at'] = datetime.now(UTC).isoformat()
        try:
            result = self.collection.update_one({"id": service_id}, {"$set": update_data})
            if result.matched_count == 0:
                logging.warning("Service not found for update: %s", service_id)
                return None
            logging.info("Service updated: %s", service_id)
            return self.get_service_by_id(service_id) # Returns raw dict
        except errors.PyMongoError as e:
            logging.error("Error updating service %s: %s", service_id, e)
            return None

    def soft_delete_service(self, service_id: str) -> None:
        try:
            result = self.collection.update_one({"id": service_id}, {"$set": {"is_deleted": True}})
            if result.matched_count == 0:
                logging.warning("Service not found for soft delete: %s", service_id)
            else:
                logging.info("Service soft-deleted: %s", service_id)
        except errors.PyMongoError as e:
            logging.error("Error soft-deleting service %s: %s", service_id, e)
