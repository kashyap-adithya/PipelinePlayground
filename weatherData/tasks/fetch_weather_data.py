import requests
import pandas as pd
from airflow.utils.dates import days_ago
from config.settings import WEATHER_API_KEY, BASE_URL

def fetch_weather_data(cities, ti):
    weather_data = []
    for city in cities:
        response = requests.get(BASE_URL, params={"key": WEATHER_API_KEY, "q": city, "dt": "{{ ds }}"})
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "City": data["location"]["name"],
                "Temperature": data["current"]["temp_c"],
                "Humidity": data["current"]["humidity"],
                "Condition": data["current"]["condition"]["text"],
                "Last Updated": data["current"]["last_updated"],
            })
        else:
            raise ValueError(f"Failed to fetch data for {city}: {response.status_code}")

    df = pd.DataFrame(weather_data)
    ti.xcom_push(key='weather_data', value=df.to_dict('records'))