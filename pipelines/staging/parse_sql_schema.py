# This file will take the SQLServer code that came with the dataset and parse it into postgresSQL code.

import re # Provides regular expression parsing
import psycopg
from pathlib import Path
from pipelines.common import paths

AW_data_folder = paths.DATA_FOLDER / "AdventureWorks-oltp-install-script"
sql_file = AW_data_folder / "instawdb.sql" 
sql_code = sql_file.read_text(encoding="utf-8")

def build_create_table_sql(table_name, columns):
  postgres_columns = []
  
  for column_name, sql_type, type_size in columns:
    postgres_type = column_type_overrides.get(
        column_name.lower(),
        type_mapping.get(sql_type.lower(), "TEXT")
    )
    
    if type_size and type_size.lower() == "max":
      postgres_type = "TEXT"
    elif type_size and postgres_type == "VARCHAR": # Adds sizes such as VARCHAR(60)
      postgres_type = f"VARCHAR({type_size})"
    
      
    postgres_column_name = (
      column_name.strip().lower().replace(" ","_")
    )
      
    postgres_columns.append(
      f'"{postgres_column_name.lower()}" {postgres_type}'
    )
    
  column_sql = ",\n".join(postgres_columns)
  
  return (
    f"CREATE TABLE IF NOT EXISTS staging."
    f"{table_name.lower()} (\n"
    f"{column_sql}\n"
    ");"
  )

# pg types matching T-SQL types
type_mapping = {
    "int": "INTEGER",
    "smallint": "SMALLINT",
    "tinyint": "SMALLINT",
    "decimal": "NUMERIC",
    "numeric": "NUMERIC",
    "money": "NUMERIC(19, 4)",
    "nvarchar": "VARCHAR",
    "datetime": "TIMESTAMP",
    "uniqueidentifier": "UUID",
    "geography": "TEXT",
}
column_type_overrides = {
    "stockedqty": "INTEGER",
}

# Describes the beginning and end of the tables
table_pattern = (
    r"CREATE TABLE "
    r"\[(?P<source_schema>[^\]]+)\]\."
    r"\[(?P<table_name>[^\]]+)\]\("
    r"(?P<table_body>.*?)"
    r"\r?\n\) ON \[PRIMARY\];"
)

tables = re.findall(
  table_pattern,
  sql_code,
  re.DOTALL,
)

column_pattern =  (
    r"^\s*\[([^\]]+)\]\s+" #column_name
    r"\[?([a-zA-Z]+)\]?" #sql_type
    r"(?:\(([^)]*)\))?" #type_size
  )
#for source_schema, table_name, table_body in tables:
#  print(source_schema, table_name)

# Matching CSV names to tables inside the sql server code
csv_files = sorted(AW_data_folder.glob("*.csv"))
csv_names = {csv_file.stem.lower() for csv_file in csv_files}

def generate_staging_sql():
  generated_sql = []
  for match in re.finditer(table_pattern, sql_code, re.DOTALL):
    table_name = match.group("table_name")
    table_body = match.group("table_body")
    
    if table_name.lower() not in csv_names:
      continue

    columns = re.findall(
        column_pattern,
        table_body,
        re.MULTILINE,
      )
    
    # print(f"\n {table_name}: CSV found")
    
    create_table_sql = build_create_table_sql(table_name, columns)
    generated_sql.append(create_table_sql)
  
  return "\n".join(generated_sql)
  
