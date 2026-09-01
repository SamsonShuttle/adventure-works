# This scripts job is to run the initial sql code that sets up the sql schemas and other helper tables.

import os                               # Import pythons built in operating system module, so it can interact with computer
import psycopg                          # Module for working with postgres db.
from dotenv import load_dotenv          # Allows py to load variables from .env file
from pathlib import Path                # Path is used to work on folder paths in an easier way

load_dotenv()  

try:
  conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
  )
  with conn.cursor() as cursor: # This opens the connection, db code runs inside this block. connection closes when py leaves block
      cursor.execute("SELECT current_database(), current_user;")
      database, user = cursor.fetchone()
      print(f"Connected to {database} as {user}")
except psycopg.Error as error:
  print(f"Database error: {error}")

# Project helpers
project_root = Path(__file__).resolve().parents[1] # __file__ is the path of this file. .resolve() converts to absolute path. .parents[1] moves it up to pipelines. folder
sql_folder = project_root / "sql"
  
# Function that will loop over the sql_files and execute them
def execute_sql_file(connection, sql_files):
  for sql_file in sql_files:
    print(f"Running {sql_file.name}")
    sql_code = sql_file.read_text(encoding="utf-8") # Reads the sql file using utf-8 characters
  
    try:
      with connection.cursor() as cur:
        cur.execute(sql_code)
        print(f"{sql_file.name} complete")
    except (OSError, psycopg.Error) as error: # OSError handles file errors, psycopg handles pg errors
      print(f"{sql_file.name} failed: {error}")
      raise
  
  
schema_sql_file = sql_folder / "01_create_schemas.sql" # This is a path to the sql folder 01 schema file
ingest_sql_file = sql_folder / "02_create_ingest_tables.sql" 

sql_files = [schema_sql_file, ingest_sql_file]

execute_sql_file(conn, sql_files)
conn.commit()
print("All SQL files committed successfully")
conn.close()



