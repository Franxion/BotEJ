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

