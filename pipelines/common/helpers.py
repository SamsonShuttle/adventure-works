import os                               # Import pythons built in operating system module, so it can interact with computer
import psycopg                          # Module for working with postgres db.
from dotenv import load_dotenv          # Allows py to load variables from .env file
from pathlib import Path                # Path is used to work on folder paths in an easier way


load_dotenv()  

# Main connection to db
def postgres_db_connection():
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
        print("\n")
        print("="*100)
        print(f"Connected to {database} as {user}")
        print("="*100)
        return conn
      
  except psycopg.Error as error:
    print(f"Database error: {error}")
    raise
    
def execute_sql_code(connection, sql_code, title=None):
    try:
      with connection.cursor() as cur:
        cur.execute(sql_code)
        
        label = title or "SQL"
        print(f"{label} code complete \n")

        
    except (OSError, psycopg.Error) as error: # OSError handles file errors, psycopg handles pg errors
      print(f"SQL Code failed: {error}")
      raise
    
def execute_sql_file(connection, sql_files):
  for sql_file in sql_files:
    print(f"Running {sql_file.name}")
    sql_code = sql_file.read_text(encoding="utf-8") # Reads the sql file using utf-8 characters
  
    execute_sql_code(connection, sql_code, sql_file.name)