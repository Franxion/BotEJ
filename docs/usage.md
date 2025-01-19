# Usage Documentation / Documentazione d'Uso

## English Version

### Getting Started

The EasyJet Flight Fare Tracker is a command-line application that helps you monitor flight prices over time. Before running the application, ensure you have completed the installation steps in the development documentation.

### Basic Usage

The simplest way to run the application is with default settings:

```bash
python main.py
```

This will search for flights from Zurich (ZRH) to Rome (FCO) for the next three days using EUR as the currency. The results will be saved in the `data` directory.

### Command Line Arguments

You can customize the search using various command line arguments. Here's a comprehensive explanation of each option:

1. **Date Selection**
   ```bash
   python main.py --start-date 2025-02-01 --days 5
   ```
   This command will search for flights starting from February 1st, 2025, and look ahead for 5 days. The start date must be in YYYY-MM-DD format. If not specified, tomorrow's date is used as the default start date.

2. **Airport Selection**
   ```bash
   python main.py --departure-airport LGW --arrival-airport BCN
   ```
   This searches for flights from London Gatwick to Barcelona. Airport codes must be valid IATA codes.

3. **Currency Selection**
   ```bash
   python main.py --currency GBP
   ```
   This will display prices in British Pounds instead of the default Euro.

4. **Custom Output Location**
   ```bash
   python main.py --output-dir "my_flight_data"
   ```
   This saves the results in a custom directory instead of the default `data` directory.

### Advanced Usage Example

Here's a complete example that combines multiple options:

```bash
python main.py --start-date 2025-03-15 --days 7 --departure-airport LHR --arrival-airport CDG --currency GBP --output-dir "london_paris_march"
```

This command will:
- Search for flights from London Heathrow to Paris Charles de Gaulle
- Look at dates from March 15th, 2025, for 7 days
- Show prices in British Pounds
- Save results in a directory called "london_paris_march"

### Understanding the Output

The application saves results in JSON format. Each file contains:
- The URL used for the API request
- HTTP status code
- Any error messages (if applicable)
- Flight data including:
  - Flight numbers
  - Departure and arrival times
  - Prices for outbound and return flights
  - Flight duration

Example of reading the results:
```python
from src.data_manager import DataManager

# Initialize the data manager
dm = DataManager()

# Load results from a specific file
results = dm.load_results("my_flight_data.json")

# Access the first response's data
for flight in results[0].data:
    print(f"Flight {flight.flight_number}: {flight.outbound_price} EUR")
```

### Error Handling

The application handles several common errors:
- Invalid date formats: Will show a helpful message explaining the correct format
- Network errors: Will log the error and continue with the next request
- Invalid airport codes: Will show an error message and exit
- File system errors: Will create directories if they don't exist

If you encounter an error, check the `easyjet_api.log` file for detailed information.

---

## Versione Italiana

### Iniziare

EasyJet Flight Fare Tracker è un'applicazione da riga di comando che ti aiuta a monitorare i prezzi dei voli nel tempo. Prima di eseguire l'applicazione, assicurati di aver completato i passaggi di installazione nella documentazione di sviluppo.

### Uso Base

Il modo più semplice per eseguire l'applicazione è con le impostazioni predefinite:

```bash
python main.py
```

Questo cercherà voli da Zurigo (ZRH) a Roma (FCO) per i prossimi tre giorni utilizzando EUR come valuta. I risultati verranno salvati nella directory `data`.

### Argomenti da Riga di Comando

Puoi personalizzare la ricerca utilizzando vari argomenti da riga di comando. Ecco una spiegazione completa di ogni opzione:

1. **Selezione Data**
   ```bash
   python main.py --start-date 2025-02-01 --days 5
   ```
   Questo comando cercherà voli a partire dal 1° febbraio 2025 e guarderà avanti per 5 giorni. La data di inizio deve essere nel formato YYYY-MM-DD. Se non specificata, viene utilizzata la data di domani come data di inizio predefinita.

2. **Selezione Aeroporto**
   ```bash
   python main.py --departure-airport LGW --arrival-airport BCN
   ```
   Questo cerca voli da London Gatwick a Barcellona. I codici aeroportuali devono essere codici IATA validi.

3. **Selezione Valuta**
   ```bash
   python main.py --currency GBP
   ```
   Questo mostrerà i prezzi in Sterline britanniche invece dell'Euro predefinito.

4. **Posizione Output Personalizzata**
   ```bash
   python main.py --output-dir "miei_dati_voli"
   ```
   Questo salva i risultati in una directory personalizzata invece della directory `data` predefinita.

### Esempio di Uso Avanzato

Ecco un esempio completo che combina più opzioni:

```bash
python main.py --start-date 2025-03-15 --days 7 --departure-airport LHR --arrival-airport CDG --currency GBP --output-dir "londra_parigi_marzo"
```

Questo comando:
- Cercherà voli da London Heathrow a Paris Charles de Gaulle
- Guarderà le date dal 15 marzo 2025 per 7 giorni
- Mostrerà i prezzi in Sterline britanniche
- Salverà i risultati in una directory chiamata "londra_parigi_marzo"

### Comprendere l'Output

L'applicazione salva i risultati in formato JSON. Ogni file contiene:
- L'URL utilizzato per la richiesta API
- Codice di stato HTTP
- Eventuali messaggi di errore (se applicabile)
- Dati dei voli inclusi:
  - Numeri di volo
  - Orari di partenza e arrivo
  - Prezzi per voli di andata e ritorno
  - Durata del volo

Esempio di lettura dei risultati:
```python
from src.data_manager import DataManager

# Inizializza il data manager
dm = DataManager()

# Carica risultati da un file specifico
risultati = dm.load_results("miei_dati_voli.json")

# Accedi ai dati della prima risposta
for volo in risultati[0].data:
    print(f"Volo {volo.flight_number}: {volo.outbound_price} EUR")
```

### Gestione degli Errori

L'applicazione gestisce diversi errori comuni:
- Formati data non validi: Mostrerà un messaggio utile che spiega il formato corretto
- Errori di rete: Registrerà l'errore e continuerà con la richiesta successiva
- Codici aeroportuali non validi: Mostrerà un messaggio di errore e uscirà
- Errori del filesystem: Creerà le directory se non esistono

Se incontri un errore, controlla il file `easyjet_api.log` per informazioni dettagliate.