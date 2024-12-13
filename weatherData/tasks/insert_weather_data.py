from airflow.providers.postgres.hooks.postgres import PostgresHook

def insert_weather_data_into_postgres(ti):
    weather_data = ti.xcom_pull(key='weather_data', task_ids='fetch_weather_data')
    if not weather_data:
        raise ValueError("No weather data found")

    postgres_hook = PostgresHook(postgres_conn_id='weather_postgres_connection')
    insert_query = """
    INSERT INTO weather_data (city, temperature, humidity, condition, last_updated)
    VALUES (%s, %s, %s, %s, %s)
    """
    for record in weather_data:
        postgres_hook.run(insert_query, parameters=(
            record['City'], 
            record['Temperature'], 
            record['Humidity'], 
            record['Condition'], 
            record['Last Updated']
        ))
