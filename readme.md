# EasyJet Flight Fare Tracker

[English](#english) | [Italiano](#italiano)

# English

A Python application that helps you track and analyze EasyJet flight fares over time. This project demonstrates important software development concepts including API interaction, data management, and modular application design.

# EasyJet Flight Fare Tracker

A Python application that helps you track and analyze EasyJet flight fares over time. This project demonstrates important software development concepts including API interaction, data management, and modular application design.

## Project Overview

Have you ever wondered how flight prices change over time? This application helps answer that question by automatically collecting and analyzing EasyJet flight fares. It's designed to be both a practical tool and a learning resource for understanding how modern web APIs and data processing work.

### Key Features

The application allows you to:
- Search for flights across multiple dates
- Compare prices between different routes
- Save fare data for historical analysis
- Configure searches with custom parameters
- Handle API responses reliably and safely

### Why This Project Matters

Understanding how to interact with web APIs and process data is a crucial skill in modern software development. This project provides hands-on experience with:
- Real-world API interaction
- Data modeling and transformation
- Error handling and logging
- Configuration management
- Command-line interface design

## Getting Started

### Prerequisites

Before you begin, ensure you have Python 3.8 or higher installed. You can check your Python version by running:

```bash
python --version
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/easyjet-fare-tracker.git
   cd easyjet-fare-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

The simplest way to start is by running:

```bash
python main.py
```

This will search for flights using default settings (Zurich to Rome for the next three days). To customize your search:

```bash
python main.py --start-date 2025-02-01 --days 5 --departure-airport LHR --arrival-airport CDG
```

For more detailed usage instructions, see our [Usage Documentation](docs/usage.md).

## Project Structure

The project is organized into several modules, each with a specific responsibility:

```
easyjet-fare-tracker/
├── src/
│   ├── api_client.py    # Handles API communication
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration management
│   ├── data_manager.py # Data persistence
│   └── models.py       # Data structures
├── docs/
│   ├── api.md          # API documentation
│   ├── development.md  # Development guide
│   └── usage.md        # Usage instructions
├── main.py             # Application entry point
└── requirements.txt    # Project dependencies
```

Each module is designed to be independent and focused on a single responsibility, making the code easier to understand and maintain.

## Understanding the Code

Let's look at a simple example of how the components work together:

```python
from src.api_client import EasyJetAPIClient
from src.config import APIConfig
from src.data_manager import DataManager

# Create a configuration
config = APIConfig.get_default_config(
    currency="EUR",
    departure="ZRH",
    arrival="FCO"
)

# Initialize the API client
client = EasyJetAPIClient(config)

# Fetch fares for a specific date
response = client.fetch_fares_for_date("2025-02-01")

# Save the results
data_manager = DataManager()
data_manager.save_results([response])
```

This example demonstrates how the different components collaborate while maintaining clear boundaries of responsibility.

## Learning From This Project

Here are some key learning opportunities this project provides:

1. **API Interaction**: Learn how to make HTTP requests, handle responses, and manage rate limiting.
2. **Data Modeling**: Understand how to structure data using classes and dataclasses in Python.
3. **Error Handling**: See practical examples of robust error handling and logging.
4. **Configuration Management**: Learn how to manage application settings effectively.
5. **Code Organization**: Study how to structure a Python project for maintainability.

## Documentation

For more detailed information, check out:
- [Development Guide](docs/development.md) - Setting up your development environment
- [Usage Guide](docs/usage.md) - Detailed usage instructions


---

# Italiano

Un'applicazione Python che ti aiuta a monitorare e analizzare le tariffe dei voli EasyJet nel tempo. Questo progetto dimostra importanti concetti di sviluppo software tra cui l'interazione con le API, la gestione dei dati e la progettazione modulare delle applicazioni.

## Panoramica del Progetto

Ti sei mai chiesto come cambiano i prezzi dei voli nel tempo? Questa applicazione aiuta a rispondere a questa domanda raccogliendo e analizzando automaticamente le tariffe dei voli EasyJet. È progettata per essere sia uno strumento pratico che una risorsa di apprendimento per capire come funzionano le moderne API web e l'elaborazione dei dati.

### Caratteristiche Principali

L'applicazione ti permette di:
- Cercare voli su più date
- Confrontare i prezzi tra diverse rotte
- Salvare i dati delle tariffe per analisi storiche
- Configurare ricerche con parametri personalizzati
- Gestire le risposte API in modo affidabile e sicuro

### Perché Questo Progetto è Importante

Comprendere come interagire con le API web ed elaborare i dati è una competenza cruciale nello sviluppo software moderno. Questo progetto fornisce esperienza pratica con:
- Interazione con API del mondo reale
- Modellazione e trasformazione dei dati
- Gestione degli errori e logging
- Gestione della configurazione
- Progettazione dell'interfaccia a riga di comando

## Per Iniziare

### Prerequisiti

Prima di iniziare, assicurati di avere Python 3.8 o superiore installato. Puoi verificare la tua versione di Python eseguendo:

```bash
python --version
```

### Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuousername/easyjet-fare-tracker.git
   cd easyjet-fare-tracker
   ```

2. Crea e attiva un ambiente virtuale:
   ```bash
   # Su Windows
   python -m venv venv
   venv\Scripts\activate

   # Su macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Uso Base

Il modo più semplice per iniziare è eseguire:

```bash
python main.py
```

Questo cercherà voli usando le impostazioni predefinite (da Zurigo a Roma per i prossimi tre giorni). Per personalizzare la tua ricerca:

```bash
python main.py --start-date 2025-02-01 --days 5 --departure-airport LHR --arrival-airport CDG
```

Per istruzioni d'uso più dettagliate, consulta la nostra [Documentazione d'Uso](docs/usage.md).

## Struttura del Progetto

Il progetto è organizzato in diversi moduli, ognuno con una responsabilità specifica:

```
easyjet-fare-tracker/
├── src/
│   ├── api_client.py    # Gestisce la comunicazione API
│   ├── cli.py          # Interfaccia riga di comando
│   ├── config.py       # Gestione configurazione
│   ├── data_manager.py # Persistenza dei dati
│   └── models.py       # Strutture dati
├── docs/
│   ├── api.md          # Documentazione API
│   ├── development.md  # Guida allo sviluppo
│   └── usage.md        # Istruzioni d'uso
├── main.py             # Punto di ingresso applicazione
└── requirements.txt    # Dipendenze del progetto
```

Ogni modulo è progettato per essere indipendente e concentrato su una singola responsabilità, rendendo il codice più facile da capire e mantenere.

## Comprendere il Codice

Vediamo un esempio semplice di come i componenti lavorano insieme:

```python
from src.api_client import EasyJetAPIClient
from src.config import APIConfig
from src.data_manager import DataManager

# Crea una configurazione
config = APIConfig.get_default_config(
    currency="EUR",
    departure="ZRH",
    arrival="FCO"
)

# Inizializza il client API
client = EasyJetAPIClient(config)

# Recupera le tariffe per una data specifica
response = client.fetch_fares_for_date("2025-02-01")

# Salva i risultati
data_manager = DataManager()
data_manager.save_results([response])
```

Questo esempio dimostra come i diversi componenti collaborano mantenendo chiari i confini di responsabilità.

## Imparare da Questo Progetto

Ecco alcune opportunità di apprendimento chiave che questo progetto offre:

1. **Interazione API**: Impara come effettuare richieste HTTP, gestire risposte e gestire il rate limiting.
2. **Modellazione Dati**: Comprendi come strutturare i dati usando classi e dataclass in Python.
3. **Gestione Errori**: Vedi esempi pratici di gestione errori e logging robusti.
4. **Gestione Configurazione**: Impara come gestire efficacemente le impostazioni dell'applicazione.
5. **Organizzazione del Codice**: Studia come strutturare un progetto Python per la manutenibilità.

## Documentazione

Per informazioni più dettagliate, consulta:
- [Guida allo Sviluppo](docs/development.md) - Configurare il tuo ambiente di sviluppo
- [Guida all'Uso](docs/usage.md) - Istruzioni d'uso dettagliate

## Contribuire

I contributi sono benvenuti! Ecco come puoi aiutare:
1. Fai un fork del repository
2. Crea un branch per la feature
3. Fai le tue modifiche
4. Invia una pull request

Per maggiori dettagli sul nostro processo di sviluppo, consulta la [Documentazione di Sviluppo](docs/development.md).
