from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from .value_objects import MediaReference, Contact, Rating

@dataclass
class Vendor:
    id: str
    name: str
    contact: Contact
    rating: Rating
    status: str = 'active'
    is_verified: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    logo: Optional[MediaReference] = None
    cover_image: Optional[MediaReference] = None
    legal_name: str = ""
    business_type: str = ""
    tax_id: str = ""
    payment_terms: str = ""

    def to_dict(self):
        """Converts the Vendor dataclass instance to a dictionary, handling nested dataclasses."""
        try:
            data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')} # Exclude internal fields

            # Convert nested dataclasses to dicts
            if isinstance(self.contact, Contact):
                data['contact'] = self.contact.__dict__
            if isinstance(self.rating, Rating):
                data['rating'] = self.rating.__dict__
            if isinstance(self.logo, MediaReference):
                data['logo'] = self.logo.__dict__
            if isinstance(self.cover_image, MediaReference):
                data['cover_image'] = self.cover_image.__dict__

            # Convert datetime objects to ISO format string for JSON
            if isinstance(data['created_at'], datetime):
                data['created_at'] = data['created_at'].isoformat()
            if isinstance(data['updated_at'], datetime):
                data['updated_at'] = data['updated_at'].isoformat()
            
            return data
        except Exception as e:
            import logging
            logging.error("Error serializing Vendor to dict: %s", e)
            return {}
