import json
import logging
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from src.database import get_db
from src.scraper.models import APIResponse
from src.database.models import Flight, PriceSnapshot


class DataManager:
    """
    Handles data persistence and retrieval for flight fare data.
    Supports both file-based storage and database storage.
    """

    def __init__(self, output_dir: str = "data", use_db: bool = True):
        """
        Initialize the DataManager with specified storage options.

        Args:
            output_dir: Directory path for file storage
            use_db: Whether to use database storage (defaults to True)
        """
        self.output_dir = Path(output_dir)
        self.use_db = use_db
        self._ensure_output_directory()
        self.logger = logging.getLogger(__name__)

    def _ensure_output_directory(self) -> None:
        """Creates the output directory if it doesn't exist."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create output directory: {str(e)}")
            raise

    def _generate_filename(self, base_name: Optional[str] = None) -> str:
        """Generates a structured filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{base_name}_" if base_name else ""
        return f"{prefix}fares_{timestamp}.json"

    def save_results(self,
                     responses: List[APIResponse],
                     filename: Optional[str] = None,
                     pretty_print: bool = True) -> Path:
        """
        Saves API responses to storage. If use_db is True, saves to both
        database and file. Otherwise, saves only to file.

        Args:
            responses: List of API responses to save
            filename: Optional filename for file storage
            pretty_print: Whether to format JSON output

        Returns:
            Path: Path to the saved file
        """
        # Save to database if enabled
        if self.use_db:
            self._save_to_database(responses)

        # Always save to file for backup and compatibility
        return self._save_to_file(responses, filename, pretty_print)

    def _save_to_database(self, responses: List[APIResponse]) -> None:
        """
        Saves API responses to the database.
        Creates all necessary related records.

        Args:
            responses: List of API responses to save
        """
        try:
            # Get database session using context manager
            db = next(get_db())

            for response in responses:
                self.logger.info(f"Saving response to database: {response.url}")

                try:
                    # Save response and get search operation record
                    search_op = response.save_to_db(db)
                    self.logger.info(
                        f"Successfully saved search operation {search_op.id}"
                    )

                except Exception as e:
                    self.logger.error(f"Error saving response to database: {str(e)}")
                    # Roll back transaction on error
                    db.rollback()
                    raise

        except Exception as e:
            self.logger.error(f"Database operation failed: {str(e)}")
            raise
        finally:
            db.close()

    def _save_to_file(self,
                      responses: List[APIResponse],
                      filename: Optional[str] = None,
                      pretty_print: bool = True) -> Path:
        """
        Saves API responses to a JSON file.
        Maintains the original file storage functionality.

        Args:
            responses: List of API responses to save
            filename: Optional filename for the JSON file
            pretty_print: Whether to format the JSON output

        Returns:
            Path: Path to the saved file
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
                self.logger.info(f"Processing response for file storage")

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
            self.logger.error(f"Failed to save results to file: {str(e)}")
            raise

    def get_price_history(self, flight_number: str, days: int = 30) -> List[dict]:
        """
        Retrieves price history for a specific flight from the database.

        Args:
            flight_number: The flight number to look up
            days: Number of days of history to retrieve

        Returns:
            List[dict]: List of price records with timestamps
        """
        if not self.use_db:
            self.logger.warning("Database access not enabled")
            return []

        try:
            db = next(get_db())

            # Query price history
            price_history = (
                db.query(PriceSnapshot)
                .join(Flight)
                .filter(Flight.flight_number == flight_number)
                .order_by(PriceSnapshot.timestamp.desc())
                .limit(days)
                .all()
            )

            # Convert to dictionary format
            return [
                {
                    "timestamp": snapshot.timestamp,
                    "outbound_price": snapshot.outbound_price,
                    "return_price": snapshot.return_price
                }
                for snapshot in price_history
            ]

        except Exception as e:
            self.logger.error(f"Failed to retrieve price history: {str(e)}")
            return []
        finally:
            db.close()