from typing import Dict, Any, List, Optional
import uuid # Import uuid for generating unique IDs
import logging

class CatalogService:
    def __init__(self, service_repo, vendor_repo):
        self.service_repo = service_repo
        self.vendor_repo = vendor_repo

    def list_services(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 20, sort: Optional[List[tuple]] = None) -> List[Dict]:
        try:
            logging.info("Listing services with filters: %s, skip: %d, limit: %d, sort: %s", filters, skip, limit, sort)
            return self.service_repo.get_all_services(filters, skip, limit, sort)
        except Exception as e:
            logging.error("Error listing services: %s", e)
            return []

    def get_service_details(self, service_id: str) -> Optional[Dict]:
        try:
            logging.info("Fetching service details for ID: %s", service_id)
            service = self.service_repo.get_service_by_id(service_id)
            if not service:
                logging.warning("Service not found: %s", service_id)
                return None
            vendor = self.vendor_repo.get_vendor_by_id(service["vendor_id"])
            service["vendorDetails"] = vendor
            return service
        except Exception as e:
            logging.error("Error fetching service details: %s", e)
            return None

    def filter_services(self, filters: Dict[str, Any]) -> List[Dict]:
        try:
            logging.info("Filtering services with filters: %s", filters)
            return self.service_repo.filter_services(filters)
        except Exception as e:
            logging.error("Error filtering services: %s", e)
            return []

    def create_service(self, service_data: Dict[str, Any]) -> Dict:
        try:
            logging.info("Creating service with data: %s", service_data)
            if 'id' not in service_data or not service_data['id']:
                service_data['id'] = str(uuid.uuid4()) # Generate UUID
            # Optionally validate service_data here
            return self.service_repo.create_service(service_data)
        except Exception as e:
            logging.error("Error creating service: %s", e)
            return {}

    def update_service(self, service_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        try:
            logging.info("Updating service %s with data: %s", service_id, update_data)
            return self.service_repo.update_service(service_id, update_data)
        except Exception as e:
            logging.error("Error updating service: %s", e)
            return None

    def delete_service(self, service_id: str) -> None:
        try:
            logging.info("Soft-deleting service: %s", service_id)
            self.service_repo.soft_delete_service(service_id)
        except Exception as e:
            logging.error("Error soft-deleting service: %s", e)
