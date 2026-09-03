# This file is the master file that runs all the other scripts

import os                               # Import pythons built in operating system module, so it can interact with computer
import psycopg                          # Module for working with postgres db.
from dotenv import load_dotenv          # Allows py to load variables from .env file
from pathlib import Path                # Path is used to work on folder paths in an easier way

from staging import parse_sql_schema
from setup import sql_runner

load_dotenv()  

# Main connection to db
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

  
# sql initial setup 
sql_runner.execute_sql_file(conn)
sql_runner.execute_sql_code(conn, parse_sql_schema.generate_staging_sql())

conn.commit()
print("All SQL files committed successfully")
conn.close()

