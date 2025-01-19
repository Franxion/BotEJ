import logging
from datetime import datetime, timedelta
from pathlib import Path

from src.api_client import EasyJetAPIClient
from src.cli import parse_arguments
from src.config import APIConfig
from src.data_manager import DataManager

import logging
from datetime import datetime, timedelta

from src.api_client import EasyJetAPIClient
from src.config import APIConfig
from src.data_manager import DataManager
from src.cli import parse_arguments, parse_date


def main():
    """Main entry point for the EasyJet fare fetching application."""
    # Parse command line arguments
    args = parse_arguments()

    # Initialize components with custom configuration
    config = APIConfig.get_default_config(
        currency=args.currency,
        departure=args.departure_airport,
        arrival=args.arrival_airport
    )

    api_client = EasyJetAPIClient(config)
    data_manager = DataManager()

    # Parse and validate start date
    try:
        start = parse_date(args.start_date)
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        return
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    # Generate dates
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d")
             for i in range(args.days)]

    # Fetch data for all dates
    responses = []
    for date in dates:
        response = api_client.fetch_fares_for_date(date)
        responses.append(response)
        print(f"found flight{response.data}")

    # Convert the output_dir string to a Path object
    output_path = Path(args.output_dir)

    # Create the directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save results
    data_manager.save_results(responses, str(args.output_dir))
    logging.info(f"Data saved to {args.output_dir}")


if __name__ == "__main__":
    main()