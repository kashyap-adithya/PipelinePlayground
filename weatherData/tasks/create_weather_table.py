CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    temperature FLOAT,
    humidity INT,
    condition TEXT,
    last_updated TIMESTAMP
);
"""