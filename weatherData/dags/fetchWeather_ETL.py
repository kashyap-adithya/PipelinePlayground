from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from tasks.fetch_weather_data import fetch_weather_data
from tasks.insert_weather_data import insert_weather_data_into_postgres
from tasks.create_weather_table import CREATE_TABLE_SQL

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_store_weather_data',
    default_args=default_args,
    description='Fetch weather data and store it in Postgres',
    schedule_interval=timedelta(days=1),
)

fetch_weather_data_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    op_args=[["Bengaluru"]],  # List of cities
    dag=dag,
)

create_weather_table_task = PostgresOperator(
    task_id='create_weather_table',
    postgres_conn_id='weather_postgres_connection',
    sql=CREATE_TABLE_SQL,
    dag=dag,
)

insert_weather_data_task = PythonOperator(
    task_id='insert_weather_data',
    python_callable=insert_weather_data_into_postgres,
    dag=dag,
)

fetch_weather_data_task >> create_weather_table_task >> insert_weather_data_task