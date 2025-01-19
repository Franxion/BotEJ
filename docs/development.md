# Development Documentation / Documentazione di Sviluppo

## English Version

### Project Overview
This project implements a Python application for fetching and analyzing EasyJet flight fares. It's structured as a modular application that demonstrates several important software development concepts including API interaction, data management, and command-line interface design.

### Current Architecture
The project follows a modular architecture with clear separation of concerns:

1. **API Client** (`api_client.py`): Handles all communication with the EasyJet API
   - Implements rate limiting through random delays
   - Manages HTTP requests and response parsing
   - Includes comprehensive error handling and logging

2. **Data Models** (`models.py`): Defines the core data structures
   - Uses dataclasses for clean, type-hinted data representations
   - Implements domain-specific logic (e.g., flight duration calculations)
   - Provides factory methods for object creation from API responses

3. **Configuration** (`config.py`): Centralizes application configuration
   - Uses dataclasses for type-safe configuration
   - Provides sensible defaults with override capabilities
   - Includes comprehensive documentation of all options

4. **Data Management** (`data_manager.py`): Handles data persistence
   - Implements JSON-based storage with proper formatting
   - Provides methods for saving and loading flight data
   - Includes error handling and logging

5. **Command Line Interface** (`cli.py`): Manages user interaction
   - Implements argument parsing with validation
   - Provides helpful defaults and documentation
   - Includes error handling for user input

### Development Setup

1. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Copy `config.py` and modify values as needed
   - Key configurations:
     - API endpoints
     - Rate limiting parameters
     - Default airports and currency

### Current Logging Implementation
The application implements comprehensive logging through Python's built-in logging module:

- Logs are written to both file (`easyjet_api.log`) and console
- Different log levels are used for different types of events:
  - INFO for regular operations
  - ERROR for operation failures
  - DEBUG for detailed troubleshooting information
- Log messages include timestamps and proper formatting

### Error Handling
The application implements robust error handling across different components:

- API communication errors in `api_client.py`
- File I/O errors in `data_manager.py`
- Input validation errors in `cli.py`
- Configuration errors in `config.py`

### Recommended Improvements

1. **Testing Implementation**
   As the project currently lacks tests, implementing a testing suite would be a valuable learning experience. Consider adding:

   - Unit tests for individual components:
     ```python
     # Example test for FlightFare class
     def test_flight_duration_calculation():
         fare = FlightFare(
             flight_number="EJ123",
             departure_airport="ZRH",
             arrival_airport="FCO",
             arrival_country="Italy",
             outbound_price=100.0,
             return_price=90.0,
             departure_datetime=datetime(2025, 1, 1, 10, 0),
             arrival_datetime=datetime(2025, 1, 1, 12, 0)
         )
         assert fare.calculate_flight_duration() == 2.0
     ```

2. **Additional Features**
   - Implement response caching to reduce API calls
   - Add data analysis capabilities
   - Create a web interface
   - Add support for multiple airlines

3. **Code Quality Improvements**
   - Add type hints throughout the codebase
   - Implement input validation for all user-provided data
   - Add more comprehensive error recovery mechanisms

---

## Versione Italiana

### Panoramica del Progetto
Questo progetto implementa un'applicazione Python per recuperare e analizzare le tariffe dei voli EasyJet. È strutturato come un'applicazione modulare che dimostra diversi importanti concetti di sviluppo software, tra cui l'interazione con le API, la gestione dei dati e la progettazione dell'interfaccia da riga di comando.

### Architettura Attuale
Il progetto segue un'architettura modulare con una chiara separazione delle responsabilità:

1. **Client API** (`api_client.py`): Gestisce tutte le comunicazioni con l'API EasyJet
   - Implementa la limitazione delle richieste attraverso ritardi casuali
   - Gestisce le richieste HTTP e l'analisi delle risposte
   - Include gestione degli errori e logging completi

2. **Modelli di Dati** (`models.py`): Definisce le strutture dati principali
   - Utilizza dataclass per rappresentazioni dei dati pulite e tipizzate
   - Implementa logica specifica del dominio (es. calcoli durata volo)
   - Fornisce metodi factory per la creazione di oggetti dalle risposte API

3. **Configurazione** (`config.py`): Centralizza la configurazione dell'applicazione
   - Utilizza dataclass per configurazioni type-safe
   - Fornisce valori predefiniti sensati con possibilità di override
   - Include documentazione completa di tutte le opzioni

4. **Gestione Dati** (`data_manager.py`): Gestisce la persistenza dei dati
   - Implementa storage basato su JSON con formattazione appropriata
   - Fornisce metodi per salvare e caricare dati dei voli
   - Include gestione degli errori e logging

5. **Interfaccia Riga di Comando** (`cli.py`): Gestisce l'interazione utente
   - Implementa parsing degli argomenti con validazione
   - Fornisce valori predefiniti e documentazione utili
   - Include gestione degli errori per input utente

### Configurazione Sviluppo

1. **Configurazione Ambiente**
   ```bash
   # Crea e attiva ambiente virtuale
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   
   # Installa dipendenze
   pip install -r requirements.txt
   ```

2. **Configurazione**
   - Copia `config.py` e modifica i valori secondo necessità
   - Configurazioni chiave:
     - Endpoint API
     - Parametri di rate limiting
     - Aeroporti e valuta predefiniti

### Implementazione Logging Attuale
L'applicazione implementa logging completo attraverso il modulo logging di Python:

- I log vengono scritti sia su file (`easyjet_api.log`) che su console
- Vengono utilizzati diversi livelli di log per diversi tipi di eventi:
  - INFO per operazioni regolari
  - ERROR per fallimenti delle operazioni
  - DEBUG per informazioni dettagliate di troubleshooting
- I messaggi di log includono timestamp e formattazione appropriata

### Gestione Errori
L'applicazione implementa una robusta gestione degli errori in diversi componenti:

- Errori di comunicazione API in `api_client.py`
- Errori di I/O su file in `data_manager.py`
- Errori di validazione input in `cli.py`
- Errori di configurazione in `config.py`

### Miglioramenti Consigliati

1. **Implementazione Test**
   Dato che il progetto attualmente non include test, implementare una suite di test sarebbe un'esperienza di apprendimento preziosa. Considerare di aggiungere:

   - Test unitari per componenti individuali:
     ```python
     # Esempio di test per la classe FlightFare
     def test_calcolo_durata_volo():
         tariffa = FlightFare(
             flight_number="EJ123",
             departure_airport="ZRH",
             arrival_airport="FCO",
             arrival_country="Italy",
             outbound_price=100.0,
             return_price=90.0,
             departure_datetime=datetime(2025, 1, 1, 10, 0),
             arrival_datetime=datetime(2025, 1, 1, 12, 0)
         )
         assert tariffa.calculate_flight_duration() == 2.0
     ```

2. **Funzionalità Aggiuntive**
   - Implementare caching delle risposte per ridurre le chiamate API
   - Aggiungere capacità di analisi dati
   - Creare un'interfaccia web
   - Aggiungere supporto per più compagnie aeree

3. **Miglioramenti Qualità del Codice**
   - Aggiungere type hints in tutto il codice
   - Implementare validazione input per tutti i dati forniti dall'utente
   - Aggiungere meccanismi più completi di recupero errori