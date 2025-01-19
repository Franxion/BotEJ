# file: api_request_handler.py
import json
import requests
from utils import generate_dates


class EasyJetAPIError(Exception):
    """Eccezione personalizzata per errori API"""
    pass


def fetch_fares_for_date(url, headers, querystring, date):
    """
    Fetch fares from the API for a specific date.
    """
    try:
        querystring["departureDateFrom"] = date
        querystring["departureDateTo"] = date
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        
        result = {
            "url": response.url,
            "status_code": response.status_code,
            "data": response.json()
        }
        
        # Verifica errori nei dati
        if not result["data"]:
            raise EasyJetAPIError(f"No data returned for date {date}")
            
        return result
        
    except requests.RequestException as e:
        error_msg = f"Request failed for date {date}: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "url": url,
            "status_code": None,
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error for date {date}: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "url": url,
            "status_code": None,
            "error": error_msg
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


class EasyJetAPI:
    """Classe per gestire le richieste API di EasyJet"""
    
    BASE_URL = "https://www.easyjet.com/api/routepricing/v3/searchfares/GetAllFaresByDate"
    
    def __init__(self, departure_airport, arrival_airport, currency="CHF"):
        self.querystring = {
            "departureAirport": departure_airport,
            "arrivalAirport": arrival_airport,
            "currency": currency
        }
        self.headers = {}
    
    def fetch_fares_for_date(self, date):
        """Recupera i prezzi per una data specifica"""
        return fetch_fares_for_date(self.BASE_URL, self.headers, self.querystring.copy(), date)
    
    def fetch_fares_for_dates(self, start_date, num_days):
        """Recupera i prezzi per un intervallo di date"""
        return fetch_fares_for_dates(self.BASE_URL, self.headers, self.querystring.copy(), 
                                   start_date, num_days)


def main():
    """
    Main function to orchestrate the script.
    """
    # Configurazione
    output_file = "output_file.json"
    start_date = "2025-05-04"
    num_days = 10
    
    # Creazione istanza API
    api = EasyJetAPI("ZRH", "FCO")
    
    # Recupero dati
    results = api.fetch_fares_for_dates(start_date, num_days)
    save_results_to_file(results, output_file)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()
