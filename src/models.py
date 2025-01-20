from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from .db_models import Flight as DBFlight
from .db_models import Route as DBRoute
from .db_models import Airport as DBAirport
from .db_models import Airline as DBAirline
from .db_models import PriceSnapshot as DBPriceSnapshot
from .db_models import SearchOperation as DBSearchOperation


@dataclass
class FlightFare:
    """
    Represents a single flight fare from the API response.
    This class now includes methods to convert to database models.
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
        """Creates a FlightFare instance from the raw API response data."""
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

    def to_db_models(self, db: Session) -> tuple[DBFlight, DBPriceSnapshot]:
        """
        Converts this FlightFare instance to database models.
        Creates or retrieves related database records as needed.

        Args:
            db: SQLAlchemy database session

        Returns:
            tuple: (Flight database model, PriceSnapshot database model)
        """
        # Get or create airports
        dep_airport = self._get_or_create_airport(db, self.departure_airport)
        arr_airport = self._get_or_create_airport(db, self.arrival_airport)

        # Get or create airline (EasyJet for now)
        airline = self._get_or_create_airline(db)

        # Get or create route
        route = self._get_or_create_route(db, airline.id, dep_airport.id, arr_airport.id)

        # Get or create flight
        flight = self._get_or_create_flight(db, route.id)

        return flight

    def _get_or_create_airport(self, db: Session, iata_code: str) -> DBAirport:
        """Helper method to get or create an airport record."""
        airport = db.query(DBAirport).filter(DBAirport.iata_code == iata_code).first()
        if not airport:
            # Note: In a real application, you'd want to look up actual city/country data
            airport = DBAirport(
                iata_code=iata_code,
                city=f"{iata_code} City",  # Placeholder
                country=f"{iata_code} Country"  # Placeholder
            )
            db.add(airport)
            db.commit()
            db.refresh(airport)
        return airport

    def _get_or_create_airline(self, db: Session) -> DBAirline:
        """Helper method to get or create the EasyJet airline record."""
        airline = db.query(DBAirline).filter(DBAirline.code == "EZY").first()
        if not airline:
            airline = DBAirline(
                name="EasyJet",
                code="EZY"
            )
            db.add(airline)
            db.commit()
            db.refresh(airline)
        return airline

    def _get_or_create_route(self, db: Session, airline_id: int,
                             dep_airport_id: int, arr_airport_id: int) -> DBRoute:
        """Helper method to get or create a route record."""
        route = db.query(DBRoute).filter(
            DBRoute.airline_id == airline_id,
            DBRoute.departure_airport_id == dep_airport_id,
            DBRoute.arrival_airport_id == arr_airport_id
        ).first()

        if not route:
            route = DBRoute(
                airline_id=airline_id,
                departure_airport_id=dep_airport_id,
                arrival_airport_id=arr_airport_id
            )
            db.add(route)
            db.commit()
            db.refresh(route)
        return route

    def _get_or_create_flight(self, db: Session, route_id: int) -> DBFlight:
        """Helper method to get or create a flight record."""
        flight = db.query(DBFlight).filter(
            DBFlight.route_id == route_id,
            DBFlight.flight_number == self.flight_number,
            DBFlight.departure_datetime == self.departure_datetime
        ).first()

        if not flight:
            flight = DBFlight(
                route_id=route_id,
                flight_number=self.flight_number,
                departure_datetime=self.departure_datetime,
                arrival_datetime=self.arrival_datetime
            )
            db.add(flight)
            db.commit()
            db.refresh(flight)
        return flight

    def calculate_flight_duration(self) -> float:
        """Calculates the duration of the flight in hours."""
        duration = self.arrival_datetime - self.departure_datetime
        return duration.total_seconds() / 3600


@dataclass
class APIResponse:
    """
    Represents a complete response from the API.
    Now includes methods to save to database.
    """
    url: str
    status_code: int
    data: List[FlightFare]
    error: Optional[str] = None

    @property
    def is_successful(self) -> bool:
        """Checks if the API call was successful."""
        return self.status_code == 200 and self.error is None

    def save_to_db(self, db: Session) -> DBSearchOperation:
        """
        Saves this API response and its data to the database.

        Args:
            db: SQLAlchemy database session

        Returns:
            SearchOperation: The created search operation record
        """
        # Create search operation record
        search_op = DBSearchOperation(
            successful=self.is_successful,
            error_message=self.error
        )
        db.add(search_op)
        db.commit()
        db.refresh(search_op)

        # If successful, save all flight fares
        if self.is_successful:
            for fare in self.data:
                # Get or create flight record
                flight = fare.to_db_models(db)

                # Create price snapshot
                price_snapshot = DBPriceSnapshot(
                    flight_id=flight.id,
                    search_id=search_op.id,
                    outbound_price=fare.outbound_price,
                    return_price=fare.return_price
                )
                db.add(price_snapshot)

            db.commit()

        return search_op