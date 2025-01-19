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

        Args:
            responses: List of APIResponse objects to save
            filename: Optional custom filename (will add .json if missing)
            pretty_print: Whether to format JSON with indentation

        Returns:
            Path object pointing to the saved file

        Raises:
            IOError: If file writing fails
            ValueError: If responses contain invalid data
        """
        try:
            # Generate or process filename
            if filename:
                if not filename.endswith('.json'):
                    filename = f"{filename}.json"
            else:
                filename = self._generate_filename()

            output_path = self.output_dir / filename

            # Prepare data for serialization
            serializable_data = []
            for response in responses:
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

                # Convert flight fares to dictionaries
                for fare in response.data:
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

                serializable_data.append(response_dict)

            # Write to file with proper formatting
            with output_path.open("w", encoding='utf-8') as f:
                indent = 4 if pretty_print else None
                json.dump(serializable_data, f, indent=indent, ensure_ascii=False)

            self.logger.info(f"Successfully saved data to {output_path}")
            return output_path

        except (IOError, ValueError) as e:
            self.logger.error(f"Failed to save results: {str(e)}")
            raise

    def load_results(self, filename: str) -> List[APIResponse]:
        """
        Loads previously saved results from a JSON file.

        Args:
            filename: Name of the file to load (with or without .json extension)

        Returns:
            List of APIResponse objects

        Raises:
            FileNotFoundError: If the specified file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if not filename.endswith('.json'):
            filename = f"{filename}.json"

        file_path = self.output_dir / filename

        try:
            with file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert JSON data back to APIResponse objects
            responses = []
            for response_data in data:
                fare_objects = [
                    FlightFare.from_api_response(fare)
                    for fare in response_data['data']
                ]

                response = APIResponse(
                    url=response_data['url'],
                    status_code=response_data['status_code'],
                    data=fare_objects,
                    error=response_data.get('error')
                )
                responses.append(response)

            return responses

        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
            raise