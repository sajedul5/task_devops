from flask import Flask, jsonify
import socket
import datetime
import requests
import os

app = Flask(__name__)

# Endpoint to return hostname, datetime, version, and weather data for Dhaka
@app.route('/api/hello', methods=['GET'])
def hello():
    hostname = socket.gethostname()
    current_datetime = datetime.datetime.now().strftime("%y%m%d%H%M")
    version = "1.0"

    # Fetch weather data for Dhaka from OpenWeatherMap API
    weather_api_key = os.getenv('WEATHER_API_KEY', '')  # Use the environment variable, defaulting to an empty string
    if not weather_api_key:
        return jsonify({'error': 'Weather API key not provided'})

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q=Dhaka&appid={weather_api_key}&units=metric'
    response = requests.get(weather_url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'})

    weather_data = response.json()
    dhaka_temperature = weather_data['main']['temp']
    dhaka_temp_unit = 'C'

    result = {
        'hostname': hostname,
        'datetime': current_datetime,
        'version': version,
        'weather': {
            'dhaka': {
                'temperature': dhaka_temperature,
                'temp_unit': dhaka_temp_unit
            }
        }
    }

    return jsonify(result)

# Endpoint for health checks
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
