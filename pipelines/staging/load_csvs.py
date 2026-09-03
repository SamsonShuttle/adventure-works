# This file will loop through the .csv data sets we have and add them to the pg db. This is a raw/bronze level so no transformations will be done here.

from pathlib import Path
import csv

project_root = Path(__file__).resolve().parents[2]
data_folder = project_root / "data" / "AdventureWorks-oltp-install-script"

csv_files = sorted(data_folder.glob("*.csv")) # Sorted finds every file ending with .csv. .glob finds the file using filename pattern.

print(f"Found {len(csv_files)} csv files")

def csv_data_staging(csv_files=csv_files):
  for csv_file in csv_files:
    print(csv_file.name)
    
first_csv = csv_files[0]

with first_csv.open("r", encoding="utf-8", newline="") as file:
  reader = csv.DictReader(file) # Reads each row as a dictionary using the header names
  rows = list(reader) # Loads the rows so we can count them
  
print(f"/nInspecting: {first_csv.name}")
print(f"Columns: {reader.fieldnames}")
print(f"Row count: {len(rows)}")