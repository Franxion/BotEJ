import logging
from random import uniform
from time import sleep
from typing import Optional
import requests
from datetime import datetime

from src.config import APIConfig
from .models import APIResponse, FlightFare
from src.database.models import SearchOperation
logger = logging.getLogger(__name__)


class EasyJetAPIClient:
    """Client for interacting with the EasyJet API."""

    def __init__(self, config: APIConfig):
        self.config = config
        self.min_delay = config.min_delay
        self.max_delay = config.max_delay
        self._setup_logging()

    def _setup_logging(self):
        """
        Configura un logger semplice ma efficace per il client API.
        Scrive sia su file che su console con un formato chiaro.
        """
        # Crea logger con nome del modulo
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Se il logger ha già degli handler, evitiamo duplicati
        if self.logger.handlers:
            return

        # Formato comune per tutti i log
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        # Handler per file
        file_handler = logging.FileHandler('easyjet_api.log')
        file_handler.setFormatter(formatter)

        # Handler per console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Aggiunge entrambi gli handler
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _random_delay(self) -> None:
        """
        Introduce una pausa casuale tra le richieste.
        Il delay è uniforme tra min_delay e max_delay secondi.
        """
        delay = uniform(self.min_delay, self.max_delay)
        self.logger.debug(f"Random delay: waiting {delay:.2f} sec")
        sleep(delay)

    def fetch_fares_for_date(
            self,
            date: str,
            departure: Optional[str] = None,
            arrival: Optional[str] = None
    ) -> APIResponse:
        """
        Fetch fares from the API for a specific date.
        """
        self._random_delay()

        try:
            querystring = {
                "departureAirport": departure or self.config.default_departure,
                "arrivalAirport": arrival or self.config.default_arrival,
                "currency": self.config.currency,
                "departureDateFrom": date,
                "departureDateTo": date
            }

            # Log the complete request details
            logger.info(f"Making request to EasyJet API:")
            logger.info(f"URL: {self.config.base_url}")
            logger.info(f"Headers: {self.config.headers}")
            logger.info(f"Query parameters: {querystring}")

            response = requests.get(
                self.config.base_url,
                headers=self.config.headers,
                params=querystring
            )
            response.raise_for_status()

            # Log the raw response
            raw_response = response.text
            logger.info(f"Raw API response: {raw_response}")

            # Parse the JSON response
            json_data = response.json()
            logger.info(f"Parsed JSON data: {json_data}")

            # If we get here, we have valid JSON. Let's examine its structure
            if isinstance(json_data, list):
                logger.info(f"Response is a list with {len(json_data)} items")
            elif isinstance(json_data, dict):
                logger.info(f"Response is a dictionary with keys: {json_data.keys()}")
            else:
                logger.info(f"Response is of type: {type(json_data)}")

            # Convert raw API data to FlightFare objects
            fares = []
            for fare in json_data:
                try:
                    fare_obj = FlightFare.from_api_response(fare)
                    fares.append(fare_obj)
                    logger.info(f"Successfully processed fare: {fare}")
                except KeyError as e:
                    logger.error(f"Missing key in fare data: {e}")
                    logger.error(f"Problematic fare data: {fare}")
                except Exception as e:
                    logger.error(f"Error processing fare: {str(e)}")
                    logger.error(f"Problematic fare data: {fare}")

            logger.info(f"Processed {len(fares)} fares")

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