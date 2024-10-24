# Application-2-Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates

# File Structure
weather-monitoring-app/
│
├── static/
│   └── css/
│       └── style.css            # Custom CSS for styling the app
│
├── templates/
│   ├── base.html                # Base HTML template
│   ├── city_weather.html         # City-wise weather details
│   ├── daily_summary.html        # Daily summary view
│   └── alerts.html               # Weather alerts
│
├── weather_monitor.py            # Main Flask app
├── initialize_db.py              # Script to initialize the database
├── config.py                     # Configuration file (API key, etc.)
├── README.md                     # Project documentation
└── requirements.txt              # List of dependencies

# Weather Monitoring Application

This is a Flask-based weather monitoring system that retrieves weather data from the OpenWeatherMap API, processes it, stores it in a SQLite database, and provides weather summaries, city-wise weather details, and alerts when temperature exceeds a certain threshold.

## Features

- **Weather Data Collection**: Fetches weather data from OpenWeatherMap API.
- **Daily Summary**: Provides a summary of daily weather data.
- **City-Wise Weather**: Displays weather data for specific cities.
- **Alerts**: Generates alerts when the temperature exceeds a predefined threshold.
- **SQLite Integration**: Stores and processes weather data locally.

## Prerequisites

- Python 3.10+
- Flask
- SQLite
- OpenWeatherMap API Key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-monitoring-app.git
   cd weather-monitoring-app
   
## Set up a virtual environment:
python3 -m venv weather_monitor_env
source weather_monitor_env/bin/activate   # For Linux/MacOS

## Set up your OpenWeatherMap API key in the config.py file:
API_KEY = 'your_openweathermap_api_key'

## Initialize the SQLite database:
python initialize_db.py

## Run the Flask app:
python weather_monitor.py

## Visit the application in your browser at http://127.0.0.1:5000
