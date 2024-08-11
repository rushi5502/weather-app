from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from mongodb_connection import get_collection  # Adjust import if needed

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = []
    if request.method == 'POST':
        city = request.form.get('city')
        
        if not city:
            weather = {
                'city': 'N/A',
                'temperature': 'N/A',
                'description': 'No city entered',
                'icon': '01d',  # Default icon for errors or missing input
            }
            weather_data.append(weather)
        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            r = requests.get(url).json()
            
            if r.get('cod') != 200:  # If there's an error in the response
                error_message = r.get('message', 'Error fetching data')
                weather = {
                    'city': city,
                    'temperature': 'N/A',
                    'description': error_message,
                    'icon': '01d',  # Default icon for errors
                }
            else:  # If the response is successful
                weather = {
                    'city': r['name'],
                    'temperature': r['main']['temp'],
                    'description': r['weather'][0]['description'],
                    'icon': r['weather'][0]['icon'],
                }

                # Insert weather data into MongoDB
                weather_collection = get_collection('weather_data')
                weather_collection.insert_one(weather)
                
            weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
