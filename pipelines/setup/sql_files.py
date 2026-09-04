# Returns the initial SQL files that need to be setup for ELT
from pipelines.common import paths

schema_sql_file = paths.SQL_FOLDER / "01_create_schemas.sql" # This is a path to the sql folder 01 schema file
ingest_sql_file = paths.SQL_FOLDER / "02_create_ingest_tables.sql" 

sql_files = [schema_sql_file, ingest_sql_file]
  


  





