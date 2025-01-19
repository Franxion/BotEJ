from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime, timedelta


@dataclass
class APIConfig:
    """Configuration for the EasyJet API with comprehensive defaults."""
    # API-related settings
    base_url: str
    headers: Dict[str, str]

    # Flight search parameters
    currency: str
    default_departure: str
    default_arrival: str

    # Request timing settings (for rate limiting)
    min_delay: float = 0.1  # 100ms minimum delay between requests
    max_delay: float = 0.3  # 300ms maximum delay

    # Data storage settings
    output_directory: str = "data"

    @classmethod
    def get_default_config(
            cls,
            currency: Optional[str] = None,
            departure: Optional[str] = None,
            arrival: Optional[str] = None,
            min_delay: Optional[float] = None,
            max_delay: Optional[float] = None,
            output_dir: Optional[str] = None
    ) -> 'APIConfig':
        """
        Creates a configuration with default values that can be overridden.

        Args:
            currency: Optional currency code (default: EUR)
            departure: Optional departure airport code (default: ZRH)
            arrival: Optional arrival airport code (default: FCO)
            min_delay: Optional minimum delay between requests (default: 0.1)
            max_delay: Optional maximum delay between requests (default: 0.3)
            output_dir: Optional output directory path (default: "data")

        Returns:
            APIConfig: Configuration object with all settings
        """
        return cls(
            base_url="https://www.easyjet.com/api/routepricing/v3/searchfares/GetAllFaresByDate",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9"
            },
            currency=currency or "EUR",
            default_departure=departure or "ZRH",
            default_arrival=arrival or "FCO",
            min_delay=min_delay or 0.1,
            max_delay=max_delay or 0.3,
            output_directory=output_dir or "data"
        )
