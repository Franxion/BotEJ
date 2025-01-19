import json
import logging
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from src.models import APIResponse, FlightFare


class DataManager:
    """
    Handles data persistence and retrieval for flight fare data.
    Provides methods to save API responses in a structured JSON format
    and retrieve historical data for analysis.
    """

    def __init__(self, output_dir: str = "data"):
        """
        Initialize the DataManager with a specified output directory.

        Args:
            output_dir: Directory path where data files will be stored.
                       Creates the directory if it doesn't exist.
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_directory()
        self.logger = logging.getLogger(__name__)

    def _ensure_output_directory(self) -> None:
        """
        Creates the output directory if it doesn't exist.
        Raises OSError if directory creation fails.
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create output directory: {str(e)}")
            raise

    def _generate_filename(self, base_name: Optional[str] = None) -> str:
        """
        Generates a structured filename with timestamp.

        Args:
            base_name: Optional prefix for the filename

        Returns:
            String containing the generated filename with .json extension
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{base_name}_" if base_name else ""
        return f"{prefix}fares_{timestamp}.json"

    def save_results(self,
                     responses: List[APIResponse],
                     filename: Optional[str] = None,
                     pretty_print: bool = True) -> Path:
        """
        Saves API responses to a JSON file with proper formatting.
        """
        try:
            # Generate or process filename
            if filename:
                if not filename.endswith('.json'):
                    filename = f"{filename}.json"
            else:
                filename = self._generate_filename()

            output_path = self.output_dir / filename

            # Add debug logging to track the data flow
            self.logger.info(f"Processing {len(responses)} API responses")

            # Prepare data for serialization
            serializable_data = []
            for response_idx, response in enumerate(responses):
                self.logger.info(f"Processing response {response_idx + 1}")
                self.logger.info(f"Response contains {len(response.data)} flight fares")

                response_dict = {
                    "url": response.url,
                    "status_code": response.status_code,
                    "error": response.error,
                    "data": [],
                    "metadata": {
                        "saved_at": datetime.now().isoformat(),
                        "successful": response.is_successful
                    }
                }

                # Convert flight fares to dictionaries with detailed logging
                for fare_idx, fare in enumerate(response.data):
                    self.logger.info(f"Processing fare {fare_idx + 1} in response {response_idx + 1}")
                    try:
                        fare_dict = {
                            "flightNumber": fare.flight_number,
                            "departureAirport": fare.departure_airport,
                            "arrivalAirport": fare.arrival_airport,
                            "arrivalCountry": fare.arrival_country,
                            "outboundPrice": fare.outbound_price,
                            "returnPrice": fare.return_price,
                            "departureDateTime": fare.departure_datetime.isoformat(),
                            "arrivalDateTime": fare.arrival_datetime.isoformat(),
                            "flightDuration": round(fare.calculate_flight_duration(), 2)
                        }
                        response_dict["data"].append(fare_dict)
                        self.logger.info(f"Successfully processed fare {fare_idx + 1}")
                    except AttributeError as e:
                        self.logger.error(f"Failed to process fare {fare_idx + 1}: {e}")
                        self.logger.error(f"Fare object content: {vars(fare)}")
                    except Exception as e:
                        self.logger.error(f"Unexpected error processing fare {fare_idx + 1}: {e}")
                        self.logger.error(f"Fare object content: {vars(fare)}")

                serializable_data.append(response_dict)
                self.logger.info(f"Response {response_idx + 1} processed with {len(response_dict['data'])} fares")

            # Write to file with proper formatting
            with output_path.open("w", encoding='utf-8') as f:
                indent = 4 if pretty_print else None
                json.dump(serializable_data, f, indent=indent, ensure_ascii=False)

            self.logger.info(f"Successfully saved data to {output_path}")
            return output_path

        except (IOError, ValueError) as e:
            self.logger.error(f"Failed to save results: {str(e)}")
            raise
