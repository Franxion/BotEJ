import subprocess
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv


def setup_database():
    """
    Sets up the PostgreSQL database and initializes the schema.
    This script handles the complete setup process from scratch.
    """
    # Load environment variables
    load_dotenv()

    # Get database configuration from environment variables
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "flight_tracker")

    # Construct database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        # Create database if it doesn't exist
        engine = create_engine(DATABASE_URL)
        if not database_exists(engine.url):
            create_database(engine.url)
            print(f"Created database: {DB_NAME}")
        else:
            print(f"Database {DB_NAME} already exists")

        # Initialize Alembic if it hasn't been initialized
        if not os.path.exists("alembic"):
            print("Initializing Alembic...")
            subprocess.run(["alembic", "init", "alembic"], check=True)
            print("Alembic initialized successfully")

        # Create initial migration
        print("Creating initial migration...")
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True)

        # Apply migration
        print("Applying migration...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)

        # Optionally, add initial data
        print("Setup complete! Database is ready to use.")

    except Exception as e:
        print(f"Error during database setup: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
