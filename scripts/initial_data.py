from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Airline, Airport


def add_initial_data():
    """
    Adds initial required data to the database.
    This includes basic airline and airport information.
    """
    db = next(get_db())
    try:
        # Add EasyJet airline
        easyjet = Airline(
            name="EasyJet",
            code="EZY"
        )
        db.add(easyjet)

        # Add some common airports
        airports = [
            Airport(iata_code="ZRH", city="Zurich", country="Switzerland"),
            Airport(iata_code="FCO", city="Rome", country="Italy"),
            Airport(iata_code="LGW", city="London", country="United Kingdom"),
            Airport(iata_code="CDG", city="Paris", country="France")
        ]
        db.add_all(airports)

        db.commit()
        print("Initial data added successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error adding initial data: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    add_initial_data()