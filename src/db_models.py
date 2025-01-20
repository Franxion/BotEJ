from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Airport(Base):
    """
    Represents an airport in the system.
    Stores basic information about airports used in routes.
    """
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True)
    iata_code = Column(String(3), unique=True, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # Relationships
    departures = relationship("Route", foreign_keys="Route.departure_airport_id", back_populates="departure_airport")
    arrivals = relationship("Route", foreign_keys="Route.arrival_airport_id", back_populates="arrival_airport")


class Airline(Base):
    """
    Represents an airline company.
    Currently only EasyJet, but designed for future expansion.
    """
    __tablename__ = 'airlines'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String(3), unique=True, nullable=False)

    # Relationships
    routes = relationship("Route", back_populates="airline")


class Route(Base):
    """
    Represents a flight route between two airports.
    Links airports and airlines together.
    """
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    airline_id = Column(Integer, ForeignKey('airlines.id'), nullable=False)
    departure_airport_id = Column(Integer, ForeignKey('airports.id'), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey('airports.id'), nullable=False)

    # Relationships
    airline = relationship("Airline", back_populates="routes")
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_id], back_populates="departures")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_id], back_populates="arrivals")
    flights = relationship("Flight", back_populates="route")


class Flight(Base):
    """
    Represents a specific scheduled flight.
    Contains flight details and schedule information.
    """
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    flight_number = Column(String, nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)

    # Relationships
    route = relationship("Route", back_populates="flights")
    price_history = relationship("PriceSnapshot", back_populates="flight")


class SearchOperation(Base):
    """
    Records each price search operation.
    Helps track the bot's performance and reliability.
    """
    __tablename__ = 'search_operations'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    successful = Column(Boolean, nullable=False)
    error_message = Column(String, nullable=True)

    # Relationships
    prices_found = relationship("PriceSnapshot", back_populates="search")


class PriceSnapshot(Base):
    """
    Records individual price observations.
    Preserves complete price history instead of updating prices.
    """
    __tablename__ = 'price_snapshots'

    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.id'), nullable=False)
    search_id = Column(Integer, ForeignKey('search_operations.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    outbound_price = Column(Float, nullable=False)
    return_price = Column(Float, nullable=False)

    # Relationships
    flight = relationship("Flight", back_populates="price_history")
    search = relationship("SearchOperation", back_populates="prices_found")