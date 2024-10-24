import requests
import sqlite3
from flask import Flask, jsonify, render_template
from time import time
from datetime import datetime

app = Flask(__name__)

# Database setup
def connect_db():
    return sqlite3.connect('weather_data.db')

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temp REAL NOT NULL,
                feels_like REAL,
                condition TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                condition TEXT NOT NULL,
                temp REAL NOT NULL,
                threshold REAL NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                avg_temp REAL,
                max_temp REAL,
                min_temp REAL,
                dominant_condition TEXT
            )
        ''')
        conn.commit()

create_tables()

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    api_key = '62d6507aa39e403382596903c5269c4f'  # Replace with your actual OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'condition': data['weather'][0]['description']
        }
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Store weather data
def store_weather_data(city, temperature, feels_like, condition):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    print(f"Inserting weather data for {city}: Temp={temperature}, Feels like={feels_like}, Condition={condition}")

    # Insert weather data into the database
    cursor.execute('''
        INSERT INTO weather (city, temperature, feels_like, condition)
        VALUES (?, ?, ?, ?)
    ''', (city, temperature, feels_like, condition))

    # Check for alerts based on the temperature
    temperature_threshold = 30.0  # Set your temperature threshold here
    if temperature > temperature_threshold:
        alert_message = f"Alert: Temperature in {city} exceeded {temperature_threshold}°C! Current temperature: {temperature}°C"
        print(f"Generating alert: {alert_message}")  # Debug log for alerts
        
        # Insert alert into the alerts table
        cursor.execute('''
            INSERT INTO alerts (city, temperature, alert_message)
            VALUES (?, ?, ?)
        ''', (city, temperature, alert_message))

    conn.commit()
    conn.close()





# Store alerts
def store_alert(city, condition, temp, threshold):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (city, condition, temp, threshold, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        ''', (city, condition, temp, threshold, int(time())))
        conn.commit()

# Calculate and store daily summary
def calculate_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    # Using date() function to group by date
    cursor.execute('''
    INSERT INTO daily_summaries (date, avg_temp, max_temp, min_temp, dominant_condition)
    SELECT 
        date(timestamp, 'unixepoch') AS date,  -- Convert timestamp to date
        AVG(temp) AS avg_temp,
        MAX(temp) AS max_temp,
        MIN(temp) AS min_temp,
        (SELECT condition FROM weather 
         WHERE date(timestamp, 'unixepoch') = date(timestamp, 'unixepoch')
         GROUP BY condition 
         ORDER BY COUNT(*) DESC LIMIT 1) AS dominant_condition  -- Get dominant weather condition
    FROM weather 
    GROUP BY date(timestamp, 'unixepoch');
    ''')
    
    conn.commit()
    conn.close()

@app.route('/city_weather')
def city_weather():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT city, AVG(temp) as avg_temp, MAX(temp) as max_temp, MIN(temp) as min_temp, 
           GROUP_CONCAT(DISTINCT condition) as conditions
    FROM weather
    GROUP BY city;
    ''')
    
    city_weather_data = cursor.fetchall()
    conn.close()

    return render_template('city_weather.html', city_weather=city_weather_data)

def check_temperature_alerts(city, temperature):
    temperature_threshold = 14 # Set the appropriate threshold for alerts
    print(f"Checking if temperature exceeds {temperature_threshold}°C")
    if temperature > temperature_threshold:
        alert_message = f"Alert: Temperature in {city} exceeded {temperature_threshold}°C! Current temperature: {temperature}°C"
        print(f"Generating alert for {city}: {alert_message}")
        
        # Insert alert into the alerts table
        cursor.execute('''
            INSERT INTO alerts (city, temperature, alert_message)
            VALUES (?, ?, ?)
        ''', (city, temperature, alert_message))
    else:
        print(f"No alert generated for {city}. Current temperature: {temperature}°C")

        conn.commit()
        conn.close()


# Fetch and process weather data
@app.route('/get_weather_data', methods=['GET'])
def get_weather_data():
    # Assuming you have a list of cities to fetch weather data for
    cities = ['City1', 'City2', 'City3']  # Replace with actual city names
    for city in cities:
        weather = fetch_weather_data(city)  # Implement this to fetch data from API
        if weather:
            store_weather_data(weather['city'], weather['temp'], weather['feels_like'], weather['condition'])
    return jsonify({"status": "Weather data updated and alerts checked."})


# Fetch alerts
@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM alerts ORDER BY id DESC')  # Fetch alerts from the database
    alerts = cursor.fetchall()

    conn.close()

    print(f"Fetched alerts: {alerts}")  # Debug log to check if alerts are fetched

    return jsonify(alerts)  # Return alerts as JSON




# Fetch daily summaries
@app.route('/daily_summary', methods=['GET'])
def get_daily_summary():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM daily_summaries ORDER BY date DESC')
        summaries = cursor.fetchall()
    return jsonify(summaries)

# Render main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
