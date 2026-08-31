

import os                               # Import pythons built in operating system module, so it can interact with computer
import psycopg                          # Module for working with postgres db.
from dotenv import load_dotenv          # Allows py to load variables from .env file
from pathlib import Path                # Path is used to work on folder paths in an easier way

load_dotenv()

# SCHEMA SETUP
project_root = Path(__file__).resolve().parents[1] # __file__ is the path of this file. .resolve() converts to absolute path. .parents[1] moves it up to pipelines. folder
schema_sql_file = project_root / "sql" / "01_create_schemas.sql" # This is a path to the sql folder 01 schema file
schema_sql = schema_sql_file.read_text(encoding="utf-8") # Reads the sql file using utf-8 characters

def run_schema_setup(connection, schema_sql):
  with connection.cursor() as cursor:
      cursor.execute(schema_sql) # Send the sql file to pg for execution
      



try:
  with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
  ) as connection:
    with connection.cursor() as cursor: # This opens the connection, db code runs inside this block. connection closes when py leaves block
      cursor.execute("SELECT current_database(), current_user;")
      database, user = cursor.fetchone()
      print(f"Connected to {database} as {user}")
      
      # 01_SCHEMA
      run_schema_setup(connection, schema_sql)
      print("schema setup complete")
      
except psycopg.Error as error:
  print(f"Database error: {error}")
    

