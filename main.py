import logging
from datetime import datetime, timedelta

from src.api_client import EasyJetAPIClient
from src.config import APIConfig
from src.data_manager import DataManager


def main():
    """Main entry point for the EasyJet fare fetching application."""
    # Initialize components
    config = APIConfig.get_default_config()
    api_client = EasyJetAPIClient(config)
    data_manager = DataManager()

    # Set up parameters
    start_date = "2025-04-01"
    num_days = 3
    output_file = "output.json"

    # Generate dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d")
             for i in range(num_days)]

    # Fetch data for all dates
    responses = []
    for date in dates:
        response = api_client.fetch_fares_for_date(date)
        responses.append(response)

    # Save results
    data_manager.save_results(responses, output_file)
    logging.info(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()