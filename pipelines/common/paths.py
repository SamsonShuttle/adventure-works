from pathlib import Path                # Path is used to work on folder paths in an easier way

PROJECT_ROOT = Path(__file__).resolve().parents[2] # __file__ is the path of this file. .resolve() converts to absolute path. .parents[1] moves it up to pipelines. folder

SQL_FOLDER = PROJECT_ROOT / "sql"
DATA_FOLDER = PROJECT_ROOT / "data"
