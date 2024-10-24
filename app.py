from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Endpoint to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to render the alerts page
@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

# Endpoint to render the trends page
@app.route('/trends')
def trends():
    return render_template('trends.html')

# API endpoint to get weather data
@app.route('/api/weather')
def get_weather_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT city, avg_temp, dominant_condition FROM daily_summary ORDER BY date DESC LIMIT 6')
    weather_data = [
        {'city': row[0], 'temp': row[1], 'condition': row[2]}
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return jsonify(weather_data)

# API endpoint to set alert threshold
@app.route('/api/set_alert', methods=['POST'])
def set_alert():
    data = request.get_json()
    threshold = data.get('threshold')

    # You can store this threshold in your database or in-memory cache
    # For simplicity, we will just return it here
    return jsonify({'status': 'success', 'threshold': threshold})

if __name__ == '__main__':
    app.run(debug=True)
