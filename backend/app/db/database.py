import psycopg2
from pgvector.psycopg2 import register_vector

from app.core.config import settings

# Handles connection between the backend and PostgreSQL database.
# Creates database sessions that allow Python to insert and retrieve data safely.
# This file acts as the central database configuration module for the entire project.

connection = psycopg2.connect(
    dbname=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT
)

register_vector(connection)

cursor = connection.cursor()

print("Database connection established successfully.")