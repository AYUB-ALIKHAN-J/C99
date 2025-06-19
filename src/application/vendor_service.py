from typing import Dict, Any, List,Optional
import uuid # Import uuid for generating unique IDs

class VendorService:
    def __init__(self, vendor_repo):
        self.vendor_repo = vendor_repo

    def list_vendors(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Lists all active vendors."""
        return self.vendor_repo.get_all_vendors(filters)

    def get_vendor_details(self, vendor_id: str) -> Optional[Dict]:
        """Retrieves details for a single vendor."""
        return self.vendor_repo.get_vendor_by_id(vendor_id)

    def create_vendor(self, vendor_data: Dict[str, Any]) -> Dict:
        """Creates a new vendor, generating an ID if not provided."""
        if 'id' not in vendor_data or not vendor_data['id']:
            vendor_data['id'] = str(uuid.uuid4()) # Generate UUID
        # You might want to validate vendor_data against the Vendor dataclass schema here
        return self.vendor_repo.create_vendor(vendor_data)

    def update_vendor(self, vendor_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        """Updates an existing vendor."""
        return self.vendor_repo.update_vendor(vendor_id, update_data)

    def delete_vendor(self, vendor_id: str) -> None:
        """Soft-deletes a vendor."""
        self.vendor_repo.soft_delete_vendor(vendor_id)
