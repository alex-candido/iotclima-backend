# django_app/__shared/open_meteo_client.py

import os
import time
from datetime import datetime, timedelta, timezone

import requests


class OpenMeteoClient:
    BASE_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
    BASE_URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

    REQUEST_DELAY_SECONDS = 0.15

    def get_hourly_historical_weather(self, latitude: float, longitude: float, start_date: datetime, end_date: datetime):

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,pressure_msl,precipitation',
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'ms',
            'precipitation_unit': 'mm',
            'timezone': 'UTC' 
        }
        
        try:
            response = requests.get(self.BASE_URL_ARCHIVE, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            time.sleep(self.REQUEST_DELAY_SECONDS)

            return self._parse_hourly_data(data)
        except requests.exceptions.Timeout:
            print("Open-Meteo API request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Open-Meteo data: {e}")
            return None

    def _parse_hourly_data(self, data):

        hourly_data = data.get('hourly', {})
        times = hourly_data.get('time', [])
        temperatures = hourly_data.get('temperature_2m', [])
        humidities = hourly_data.get('relative_humidity_2m', [])
        wind_speeds = hourly_data.get('wind_speed_10m', [])
        wind_directions = hourly_data.get('wind_direction_10m', [])
        pressures = hourly_data.get('pressure_msl', [])
        precipitations = hourly_data.get('precipitation', [])

        records_list = []
        for i, time_str in enumerate(times):
            recorded_at_aware = datetime.fromisoformat(time_str).astimezone(timezone.utc)
            
            record = {
                'recorded_at': recorded_at_aware,
                'temperature': temperatures[i] if i < len(temperatures) else None,
                'humidity': humidities[i] if i < len(humidities) else None,
                'wind_speed': wind_speeds[i] if i < len(wind_speeds) else None,
                'wind_direction': wind_directions[i] if i < len(wind_directions) else None,
                'pressure': pressures[i] if i < len(pressures) else None,
                'rainfall': precipitations[i] if i < len(precipitations) else None,
            }
            records_list.append(record)
        return records_list