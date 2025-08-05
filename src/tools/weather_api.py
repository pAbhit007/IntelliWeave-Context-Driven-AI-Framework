import requests
from typing import Dict, Optional
from src.config.settings import OPENWEATHER_API_KEY

class WeatherAPI:
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch weather data for a given city
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def format_weather_data(self, weather_data: Dict) -> str:
        """
        Format weather data into a readable string
        """
        if not weather_data:
            return "Unable to fetch weather data"

        main = weather_data.get('main', {})
        weather = weather_data.get('weather', [{}])[0]
        
        return f"""
        City: {weather_data.get('name')}
        Temperature: {main.get('temp')}°C
        Feels like: {main.get('feels_like')}°C
        Humidity: {main.get('humidity')}%
        Weather: {weather.get('description')}
        """
