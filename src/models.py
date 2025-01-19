from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class FlightFare:
    """
    Represents a single flight fare with all its attributes.

    Using a dataclass here gives us several benefits:
    1. Automatic __init__ method
    2. Easy comparison of objects
    3. Clean string representation
    4. Immutable objects if we want them (with frozen=True)

    """
    flight_number: str
    departure_airport: str
    arrival_airport: str
    arrival_country: str
    outbound_price: float
    return_price: float
    departure_datetime: datetime
    arrival_datetime: datetime

    @classmethod
    def from_api_response(cls, data: dict) -> 'FlightFare':
        """
        Creates a FlightFare instance from the raw API response data.
        This factory method centralizes the conversion logic in one place.
        """
        return cls(
            flight_number=data['flightNumber'],
            departure_airport=data['departureAirport'],
            arrival_airport=data['arrivalAirport'],
            arrival_country=data['arrivalCountry'],
            outbound_price=float(data['outboundPrice']),
            return_price=float(data['returnPrice']),
            departure_datetime=datetime.fromisoformat(data['departureDateTime']),
            arrival_datetime=datetime.fromisoformat(data['arrivalDateTime'])
        )

    def calculate_flight_duration(self) -> float:
        """
        Calculates the duration of the flight in hours.
        This is an example of putting behavior close to the data it operates on.
        """
        duration = self.arrival_datetime - self.departure_datetime
        return duration.total_seconds() / 3600


@dataclass
class APIResponse:
    """
    Represents a complete response from the API, including metadata and results.

    This wrapper helps us handle both successful and failed API calls in a
    consistent way, and keeps all related data together.
    """
    url: str
    status_code: int
    data: List[FlightFare] # This needs typing library - we can't specify a list's content type without it
    error: Optional[str] = None # This needs typing - Optional is a special type for None-able values

    @property
    def is_successful(self) -> bool:
        """
        Checks if the API call was successful.
        Properties are a clean way to add computed attributes to our data.

        """
        return self.status_code == 200 and self.error is None