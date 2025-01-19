import logging
from typing import List, Optional
import requests
from datetime import datetime, timedelta
from src.config import APIConfig
from src.models import APIResponse, FlightFare
logger = logging.getLogger(__name__)


class EasyJetAPIClient:
    """Client for interacting with the EasyJet API."""

    def __init__(self, config: APIConfig):
        self.config = config
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the API client."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def fetch_fares_for_date(
            self,
            date: str,
            departure: Optional[str] = None,
            arrival: Optional[str] = None
    ) -> APIResponse:
        """
        Fetch fares from the API for a specific date.

        Args:
            date: Date in YYYY-MM-DD format
            departure: Optional departure airport code
            arrival: Optional arrival airport code

        Returns:
            APIResponse object containing the results or error
        """
        try:
            querystring = {
                "departureAirport": departure or self.config.default_departure,
                "arrivalAirport": arrival or self.config.default_arrival,
                "currency": self.config.currency,
                "departureDateFrom": date,
                "departureDateTo": date
            }

            logger.info(f"Fetching fares for date: {date}")
            response = requests.get(
                self.config.base_url,
                headers=self.config.headers,
                params=querystring
            )
            response.raise_for_status()

            # Convert raw API data to FlightFare objects
            fares = [FlightFare.from_api_response(fare) for fare in response.json()]

            return APIResponse(
                url=response.url,
                status_code=response.status_code,
                data=fares
            )

        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return APIResponse(
                url=self.config.base_url,
                status_code=getattr(e.response, 'status_code', None),
                data=[],
                error=str(e)
            )