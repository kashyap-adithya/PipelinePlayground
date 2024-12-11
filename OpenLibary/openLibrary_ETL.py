from datetime import datetime, timedelta
from airflow import DAG
import requests
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# 1) Fetch Open Library data (extract) 2) Clean data (transform)

def get_openlibrary_data_books(num_books, ti):
    query = "data engineering"
    url = f"https://openlibrary.org/search.json?q={query}&limit={num_books}"

    # Send a request to Open Library API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        books = [
            {
                "Title": book.get("title"),
                "Author": ", ".join(book.get("author_name", [])),
                "First Publish Year": book.get("first_publish_year"),
            }
            for book in data.get("docs", [])
        ]
        
        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(books)

        # Push the DataFrame to XCom
        ti.xcom_push(key='book_data', value=df.to_dict('records'))
    else:
        raise ValueError(f"Failed to fetch data from Open Library: {response.status_code}")

# 3) Create and store data in a table on PostgreSQL (load)

def insert_book_data_into_postgres(ti):
    book_data = ti.xcom_pull(key='book_data', task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data found")

    postgres_hook = PostgresHook(postgres_conn_id='books_connection')
    insert_query = """
    INSERT INTO books (title, authors, first_publish_year)
    VALUES (%s, %s, %s)
    """
    for book in book_data:
        postgres_hook.run(insert_query, parameters=(
            book['Title'], 
            book['Author'], 
            book['First Publish Year']
        ))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_store_openlibrary_books',
    default_args=default_args,
    description='A simple DAG to fetch book data from Open Library and store it in Postgres',
    schedule_interval=timedelta(days=1),
)

# Operators: PythonOperator and PostgresOperator
fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_openlibrary_data_books,
    op_args=[100],  # Number of books to fetch
    dag=dag,
)

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='books_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT,
        first_publish_year INT
    );
    """,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

# Dependencies
fetch_book_data_task >> create_table_task >> insert_book_data_task
