import json
from typing import List
from datetime import datetime
from pathlib import Path
from src.models import APIResponse

class DataManager:
    """Handles data persistence and retrieval."""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)


    def save_results(self, responses: List[APIResponse], filename: str):
        """
        Salva le risposte API in un file JSON.

        Args:
            responses: Lista di oggetti APIResponse da salvare
            filename: Nome del file in cui salvare i dati
        """
        # Creiamo il percorso completo del file usando pathlib
        output_path = self.output_dir / filename

        serializable_data = []

        for response in responses:
            response_dict = {
                "url": response.url,
                "status_code": response.status_code,
                "error": response.error,
                "data": []  # Questa lista conterrà i dati dei voli
            }

            for fare in response.data:
                fare_dict = {
                    "flightNumber": fare.flight_number,
                    "departureAirport": fare.departure_airport,
                    "arrivalAirport": fare.arrival_airport,
                    "arrivalCountry": fare.arrival_country,
                    "outboundPrice": fare.outbound_price,
                    "returnPrice": fare.return_price,
                    "departureDateTime": fare.departure_datetime.isoformat(),
                    "arrivalDateTime": fare.arrival_datetime.isoformat()
                }

                # Aggiungiamo questo volo alla lista dei voli di questa risposta
                response_dict["data"].append(fare_dict)

            # Aggiungiamo questa risposta alla lista principale
            serializable_data.append(response_dict)

        # Apriamo il file e salviamo tutti i dati in formato JSON
        with output_path.open("w") as f:
            # indent=4 fa sì che il JSON sia formattato in modo leggibile
            json.dump(serializable_data, f, indent=4)