import json
import requests
from dateGeneration import generate_dates  # Assuming this generates dates in "YYYY-MM-DD" format

url = "https://www.easyjet.com/api/routepricing/v3/searchfares/GetAllFaresByDate"

NUM_DAYS = 100

querystring = {
    "departureAirport": "ZRH",
    "arrivalAirport": "FCO",
    "currency": "CHF",
    # "departureDateFrom": "2025-06-10",  # Will be updated dynamically
    # "departureDateTo": "2025-06-11"   # Will be updated dynamically
}

payload = ""
headers = {
    # Uncomment and add necessary headers if required
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    # "Accept": "application/json, text/plain, */*",
    # "Accept-Language": "en-US,en;q=0.5",
}

def perform_request(url, headers, payload, querystring, output_file="output_file.txt"):
    results = []
    # Generate dates for requests
    dates = generate_dates("2025-06-10", NUM_DAYS)  # Ensure the function generates in "YYYY-MM-DD" format

    for date in dates:
        try:
            # Update querystring with dynamic dates
            querystring["departureDateFrom"] = date
            querystring["departureDateTo"] = date

            # Perform the request
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            response.raise_for_status()  # Raise error for bad status codes

            # Append processed response data
            results.append({
                "url": response.url,
                "status_code": response.status_code,
                "data": response.json()  # Assuming the API returns JSON
            })
        except requests.RequestException as e:
            print(f"Request to {url} failed: {e}")
            results.append({
                "url": url,
                "status_code": None,
                "error": str(e)
            })

    # Save results to file
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)
    print(f"Data saved to {output_file}")

# Execute the function
perform_request(url, headers, payload, querystring, output_file="output_file.txt")
print("finished")
