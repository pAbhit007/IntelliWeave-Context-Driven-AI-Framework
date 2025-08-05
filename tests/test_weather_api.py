import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.weather_api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.weather_api = WeatherAPI()

    @patch('src.tools.weather_api.requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'London',
            'main': {
                'temp': 20.5,
                'feels_like': 18.2,
                'humidity': 65
            },
            'weather': [{'description': 'clear sky'}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.weather_api.get_weather('London')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'London')
        self.assertEqual(result['main']['temp'], 20.5)

    @patch('src.tools.weather_api.requests.get')
    def test_get_weather_api_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        result = self.weather_api.get_weather('InvalidCity')
        self.assertIsNone(result)

    def test_format_weather_data_valid(self):
        weather_data = {
            'name': 'London',
            'main': {
                'temp': 20.5,
                'feels_like': 18.2,
                'humidity': 65
            },
            'weather': [{'description': 'clear sky'}]
        }
        
        formatted = self.weather_api.format_weather_data(weather_data)
        
        self.assertIn('London', formatted)
        self.assertIn('20.5°C', formatted)
        self.assertIn('clear sky', formatted)

    def test_format_weather_data_none(self):
        formatted = self.weather_api.format_weather_data(None)
        self.assertEqual(formatted, "Unable to fetch weather data")

if __name__ == '__main__':
    unittest.main()