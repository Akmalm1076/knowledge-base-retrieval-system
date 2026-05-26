import psycopg2
from pgvector.psycopg2 import register_vector
# Handles connection between the backend and PostgreSQL database.
# Creates database sessions that allow Python to insert and retrieve data safely.
# This file acts as the central database configuration module for the entire project.

connection = psycopg2.connect(
    dbname="knowledge_base",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)

register_vector(connection)

cursor = connection.cursor()

print("Database connection established successfully.")