# EasyJet Flight Price Tracker

## Project Overview
This project is a flight price tracking system that currently focuses on EasyJet flights. It scrapes flight pricing data from EasyJet's API and stores it in a PostgreSQL database for analysis. The system is designed with modularity in mind, allowing for future expansion to track other airlines.

## Project Structure
```
Bot Easyjet/
├── src/
│   ├── __init__.py
│   ├── data_manager.py    # Handles data persistence and retrieval
│   ├── cli.py            # Command line interface utilities
│   ├── config.py         # Configuration management
│   │
│   ├── database/         # Database-related modules
│   │   ├── __init__.py
│   │   ├── models.py     # SQLAlchemy database models
│   │   └── connection.py # Database connection handling
│   │
│   └── scraper/          # Web scraping components
│       ├── __init__.py
│       ├── api_client.py # EasyJet API client
│       └── models.py     # Data models for API responses
│
├── setup_database.py     # Database initialization script
├── initial_data.py      # Script to populate initial data
├── test_database.py     # Database testing utilities
└── requirements.txt     # Project dependencies
```

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd Bot-Easyjet
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your database configuration:
```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flight_tracker
```

Right now it is:
```
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flight_tracker
```

4. Set up the database:
```bash
python setup_database.py
```

5. Initialize basic data:
```bash
python initial_data.py
```

## Database Schema
The project uses a relational database with the following main tables:
- `airlines`: Stores airline information
- `airports`: Stores airport details
- `routes`: Connects airports and airlines
- `flights`: Stores flight schedule information
- `search_operations`: Records each price search operation
- `price_snapshots`: Stores historical price data

## Usage
The system can be used to:
1. Fetch current flight prices from EasyJet
2. Store pricing data in a database
3. Analyze historical price trends

Basic usage:
```bash
python main.py --departure-airport ZRH --arrival-airport FCO --start-date 2025-08-05 --days 5
```

Command line arguments:
- `--start-date`: Start date for fare search (YYYY-MM-DD)
- `--days`: Number of days to fetch fares for (default: 3)
- `--departure-airport`: Departure airport code (default: ZRH)
- `--arrival-airport`: Arrival airport code (default: FCO)
- `--currency`: Currency for fare prices (default: EUR)
- `--output-dir`: Directory to store output files (default: data)

## Testing
To verify the database functionality:
```bash
python test_database.py
```

This will run a series of tests to ensure:
- Database connectivity
- Data insertion and retrieval
- Price history tracking

## Project Status
Current Features:
- EasyJet API integration
- Automated price data collection
- Database storage of flight prices
- Basic price analysis capabilities

Future Plans:
- Support for additional airlines
- Web interface for data visualization
- Advanced price analytics
- Price prediction features

## Technical Details
- The project uses SQLAlchemy for database operations
- Alembic handles database migrations
- Data is fetched through EasyJet's public API
- Rate limiting is implemented to respect API constraints

## Notes for Developers
- The system is designed to be modular, allowing easy addition of new airlines
- API responses are cached in JSON files as backup
- Database operations are wrapped in transactions for data integrity
- The project follows Python package structure conventions

## Troubleshooting
Common issues and solutions:
1. Database connection errors:
   - Verify PostgreSQL is running
   - Check .env file configuration
   - Ensure database exists and is accessible

2. Import errors:
   - Run scripts from project root directory
   - Verify Python environment has all requirements installed

3. API errors:
   - Check internet connectivity
   - Verify API endpoint is accessible
   - Review rate limiting settings

