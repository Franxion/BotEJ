# file: api_request_handler.py
import json
import requests
from utils import generate_dates


def fetch_fares_for_date(url, headers, querystring, date):
    """
    Fetch fares from the API for a specific date.
    """
    try:
        querystring["departureDateFrom"] = date
        querystring["departureDateTo"] = date
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        return {
            "url": response.url,
            "status_code": response.status_code,
            "data": response.json()
        }
    except requests.RequestException as e:
        return {
            "url": url,
            "status_code": None,
            "error": str(e)
        }


def fetch_fares_for_dates(url, headers, querystring, start_date, num_days):
    """
    Fetch fares for multiple dates and return the results.
    """
    results = []
    dates = generate_dates(start_date, num_days)
    for date in dates:
        results.append(fetch_fares_for_date(url, headers, querystring, date))
    return results


def save_results_to_file(results, output_file):
    """
    Save results to a JSON file.
    """
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)


def main():
    """
    Main function to orchestrate the script.
    """
    url = "https://www.easyjet.com/api/routepricing/v3/searchfares/GetAllFaresByDate"
    querystring = {
        "departureAirport": "ZRH",
        "arrivalAirport": "FCO",
        "currency": "CHF"
    }
    headers = {}
    output_file = "output_file.json"
    start_date = "2025-06-10"
    num_days = 10

    results = fetch_fares_for_dates(url, headers, querystring, start_date, num_days)
    save_results_to_file(results, output_file)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()
