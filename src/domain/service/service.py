from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from .value_objects import PricingTier, ServiceAttribute, MediaReference, PricingRule, AvailabilityRule

@dataclass
class Service:
    id: str  # System should generate if not provided (e.g., UUID)
    name: Dict[str, str]
    description: Dict[str, str]
    category: str
    service_type: str = "atomic"  # "atomic", "composite", "package"
    parent_service_ids: List[str] = field(default_factory=list)  # For nesting/bundling
    related_service_ids: List[str] = field(default_factory=list)  # For upsell/dependency/related
    base_price: float = 0.0
    currency: str = "INR"
    vendor_id: str = ""
    pricing_tiers: List[PricingTier] = field(default_factory=list)
    pricing_rules: List[PricingRule] = field(default_factory=list)
    availability_rules: List[AvailabilityRule] = field(default_factory=list)
    is_on_sale: bool = False
    sale_price: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    attributes: List[ServiceAttribute] = field(default_factory=list)
    status: str = 'active'  # System default
    is_deleted: bool = False  # System default, managed for soft deletes
    created_at: datetime = field(default_factory=datetime.utcnow)  # System sets on creation
    updated_at: datetime = field(default_factory=datetime.utcnow)  # System sets on creation/update
    available_locations: List[str] = field(default_factory=list)
    images: List[MediaReference] = field(default_factory=list)
    videos: List[MediaReference] = field(default_factory=list)
    external_refs: Dict[str, Any] = field(default_factory=dict)  # For downstream/external system IDs

    def to_dict(self):
        """Converts the Service dataclass instance to a dictionary, handling nested dataclasses."""
        try:
            data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')} # Exclude internal fields
            
            # Convert nested dataclass lists to dicts
            data['pricing_tiers'] = [tier.__dict__ for tier in self.pricing_tiers]
            data['attributes'] = [attr.__dict__ for attr in self.attributes]
            data['images'] = [img.__dict__ for img in self.images]
            data['videos'] = [vid.__dict__ for vid in self.videos]
            data['pricing_rules'] = [rule.__dict__ for rule in self.pricing_rules]
            data['availability_rules'] = [rule.__dict__ for rule in self.availability_rules]

            # Convert datetime objects to ISO format string for JSON
            if isinstance(data['created_at'], datetime):
                data['created_at'] = data['created_at'].isoformat()
            if isinstance(data['updated_at'], datetime):
                data['updated_at'] = data['updated_at'].isoformat()
            
            return data
        except Exception as e:
            import logging
            logging.error("Error serializing Service to dict: %s", e)
            return {}
