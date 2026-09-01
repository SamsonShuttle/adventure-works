# This scripts job is to run the initial sql code that sets up the sql schemas and other helper tables.

import psycopg                          # Module for working with postgres db.
from pathlib import Path                # Path is used to work on folder paths in an easier way

# Project helpers
project_root = Path(__file__).resolve().parents[2] # __file__ is the path of this file. .resolve() converts to absolute path. .parents[1] moves it up to pipelines. folder
sql_folder = project_root / "sql"

schema_sql_file = sql_folder / "01_create_schemas.sql" # This is a path to the sql folder 01 schema file
ingest_sql_file = sql_folder / "02_create_ingest_tables.sql" 

sql_files = [schema_sql_file, ingest_sql_file]
  
# Function that will loop over the sql_files and execute them
def execute_sql_file(connection, sql_files=sql_files):
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
  
  




