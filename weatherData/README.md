# Weather Data ETL Pipeline

This project implements a pipeline that extracts weather data from the [WeatherAPI](https://www.weatherapi.com/), transforms it, and loads it into a PostgreSQL database. The pipeline is managed using Apache Airflow.

### Features:
- Fetch weather data for multiple cities (Mumbai, Delhi, Bangalore) from the WeatherAPI.
- Store the raw weather data in PostgreSQL.
- Perform basic transformations (e.g., storing temperature, humidity, and condition).
- Modular code structure with separate files for each task.
- Time-series data handled efficiently using PostgreSQL or TimescaleDB for optimal performance.

---

## Table of Contents:
- [Project Setup](#project-setup)
- [Requirements](#requirements)
- [File Structure](#file-structure)
- [Airflow Setup](#airflow-setup)
- [Using TimescaleDB](#using-timescaledb)
- [Running the Pipeline](#running-the-pipeline)
- [License](#license)

---

## Project Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/weather-etl-pipeline.git
   cd weather-etl-pipeline
   ```

2. **Create a virtual environment (Optional but recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows
    ```
3. **Set up PostgreSQL**:
    - Install PostgreSQL if you don't have it running locally or use a managed service.
    - Create a database (e.g., weather_data).
4. **Set up Airflow**:
    - Install Airlfow: ```bash pip install apache-airflow ```
    - Initialize the Airflow database: ```bash airflow db init ```
5. **Configure the connection to PostgreSQL in Airflow**:
    - Navigate to the Airflow UI at http://localhost:8080.
    - Go to Admin > Connections and create a new connection with the following details:
        - Connection ID: weather_postgres_connection
        - Connection Type: Postgres
        - Host: localhost (or your PostgreSQL instance)
        - Schema: weather_data
        - Login: your_postgres_user
        - Password: your_postgres_password
6. **Set up WeatherAPI credentials**:
    - Create a file config/settings.py and add your WeatherAPI key:
    ```bash 
        WEATHER_API_KEY = "your_api_key"
        BASE_URL = "http://api.weatherapi.com/v1/current.json"
    ```

## File Structure

```bash
weather-etl-pipeline/
│
├── dags/
│   ├── fetch_weather_dag.py         # Main DAG for the weather ETL pipeline
│
├── tasks/
│   ├── fetch_weather_data.py        # Fetch weather data from WeatherAPI
│   ├── insert_weather_data.py       # Insert data into PostgreSQL
│   ├── create_weather_table.py      # SQL for creating the weather data table
│
├── config/
│   ├── settings.py                  # API keys and common settings
│
├── README.md             
```