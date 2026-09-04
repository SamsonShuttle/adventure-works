# This file is the master file that runs all the other scripts

import os                               # Import pythons built in operating system module, so it can interact with computer
import psycopg                          # Module for working with postgres db.
from dotenv import load_dotenv          # Allows py to load variables from .env file
from pathlib import Path                # Path is used to work on folder paths in an easier way

from pipelines.common import helpers
from pipelines.staging import parse_sql_schema
from pipelines.setup import sql_files

conn = helpers.postgres_db_connection()

  
# sql initial setup 
helpers.execute_sql_file(conn, sql_files.sql_files)
helpers.execute_sql_code(conn, parse_sql_schema.generate_staging_sql())

conn.commit()
print("All SQL files committed successfully")
conn.close()

