from src.database import get_db
from sqlalchemy import text  # Add this import


def test_database_connection():
    try:
        # Try to get a database session
        db = next(get_db())
        print("Database connection successful!")

        # Use text() to make our SQL query explicit
        result = db.execute(text("SELECT 1"))
        print("Query executed successfully!")

        # Let's also fetch and print the result to see what we got
        value = result.scalar()
        print(f"Query returned: {value}")

        db.close()
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")


if __name__ == "__main__":
    test_database_connection()