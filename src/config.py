from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class APIConfig:
    """Configuration for the EasyJet API."""
    base_url: str
    headers: dict
    currency: str
    default_departure: str
    default_arrival: str

    @classmethod
    def get_default_config(cls) -> 'APIConfig':
        return cls(
            base_url="https://www.easyjet.com/api/routepricing/v3/searchfares/GetAllFaresByDate",
            headers={},
            currency="CHF",
            default_departure="ZRH",
            default_arrival="FCO"
        )