from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime

@dataclass
class PricingTier:
    min_quantity: int
    price: int
    currency: str

@dataclass
class ServiceAttribute:
    name: str
    value: Any
    localized: bool = False

@dataclass
class MediaReference:
    url: str
    type: str
    alt_text: Optional[Dict[str, str]] = None  # Localized text, e.g. {"en": "Haircut"}

@dataclass
class Contact:
    email: str
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None # Simplified address for now

@dataclass
class Rating:
    average: float
    count: int
    breakdown: Optional[Dict[str, int]] = None

@dataclass
class PricingRule:
    rule_type: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    price: float = 0.0
    currency: str = "INR"
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

@dataclass
class AvailabilityRule:
    conditions: Dict[str, Any] = field(default_factory=dict)
    is_available: bool = True
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
