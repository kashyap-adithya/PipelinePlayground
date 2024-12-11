# OpenLibrary DAG for Airflow

This repository contains an Apache Airflow Directed Acyclic Graph (DAG) that fetches book data from the Open Library API and stores it in a PostgreSQL database. The DAG automates the process of extracting book data, transforming it, and loading it into a structured format for further analysis.

## Features

- **Data Extraction**: Fetches book data from Open Library's API based on a specified query.
- **Data Transformation**: Cleans and prepares the data.
- **Data Loading**: Inserts the transformed data into a PostgreSQL database.
- **Reusable Components**: PythonOperator for API interaction and PostgresOperator for database tasks.

## Requirements

### Prerequisites

#### Apache Airflow
Install and configure Airflow. For setup instructions, refer to the [Airflow Documentation](https://airflow.apache.org/docs/).

#### PostgreSQL
Ensure a PostgreSQL instance is running and accessible. Create a database to store the book data.

#### Python Libraries
The DAG requires the following Python libraries:
- `requests`
- `pandas`
- `apache-airflow`
- `apache-airflow-providers-postgres`

### Configuration

Set up a PostgreSQL connection in Airflow (Admin > Connections):
- **Connection ID**: `books_connection`
- **Connection Type**: `Postgres`
- **Host, schema, login, and password** as per your PostgreSQL setup.

## DAG Overview

### Steps

1. **Fetch Book Data**  
   Uses the Open Library API to fetch details about books. The default query fetches books related to "data engineering".

2. **Create Table**  
   Creates a `books` table in the PostgreSQL database if it doesn't already exist.

3. **Insert Data**  
   Inserts the fetched book data into the PostgreSQL table.

### Dependencies
```plaintext
fetch_book_data_task >> create_table_task >> insert_book_data_task
```

### Table Schema
```sql
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    first_publish_year INT
);
```
### Example Queries
- **Query to fetch all the records**
```sql
SELECT * FROM books;
```