from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Get your API key from https://openweathermap.org/api
API_KEY = os.getenv('WEATHER_API_KEY', '6b8d3429b636eaf494b7732166f6d604')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form['city']
        if city:
            try:
                params = {
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric'  # For Celsius
                }
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                weather_data = response.json()
                
                # Process the data for display
                weather_data = {
                    'city': weather_data['name'],
                    'country': weather_data['sys']['country'],
                    'temp': weather_data['main']['temp'],
                    'feels_like': weather_data['main']['feels_like'],
                    'description': weather_data['weather'][0]['description'].capitalize(),
                    'icon': weather_data['weather'][0]['icon'],
                    'humidity': weather_data['main']['humidity'],
                    'wind': weather_data['wind']['speed']
                }
            except requests.exceptions.HTTPError:
                error = "City not found. Please try another location."
            except Exception as e:
                error = f"An error occurred: {str(e)}"
        else:
            error = "Please enter a city name"
    
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)