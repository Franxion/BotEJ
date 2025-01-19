import argparse
from datetime import datetime, timedelta


def parse_date(date_str: str) -> datetime:
    """
    Parse date string in YYYY-MM-DD format.
    Raises ValueError if format is invalid.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")


def get_default_start_date() -> str:
    """
    Returns tomorrow's date as a string in YYYY-MM-DD format.
    This provides a sensible default for flight searches.
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")


def parse_arguments() -> argparse.Namespace:
    """
    Creates and configures the command line argument parser.
    Validates the date format before returning the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="EasyJet fare fetching application.\n \
         Airport codes:\nhttps://www.easyjet.com/EN/Publishing.mvc/ShowTimetable?flyingFrom=Napoli&flyingTo=Liverpool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Date-related arguments with validation
    parser.add_argument(
        "--start-date",
        default=get_default_start_date(),
        help="Start date for fare search (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="Number of days to fetch fares for"
    )

    # Basic arguments without additional validation
    parser.add_argument(
        "--departure-airport",
        default="ZRH",
        help="Departure airport code"
    )
    parser.add_argument(
        "--arrival-airport",
        default="FCO",
        help="Arrival airport code"
    )
    parser.add_argument(
        "--currency",
        default="EUR",
        help="Currency for fare prices"
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory to store output files"
    )

    args = parser.parse_args()

    # Validate the start date after parsing
    try:
        parse_date(args.start_date)
    except ValueError as e:
        parser.error(str(e))

    return args