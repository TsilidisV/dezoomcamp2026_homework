import duckdb
import typer
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

app = typer.Typer(help="Data Ingestion CLI")

def download_and_convert_files(taxi_type, year):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)


    for month in range(1, 13):
        parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
        parquet_filepath = data_dir / parquet_filename

        if parquet_filepath.exists():
            print(f"Skipping {parquet_filename} (already exists)")
            continue

        # Download CSV.gz file
        csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
        csv_gz_filepath = data_dir / csv_gz_filename

        response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
        response.raise_for_status()

        with open(csv_gz_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Converting {csv_gz_filename} to Parquet...")
        con = duckdb.connect()
        con.execute(f"""
            COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
            TO '{parquet_filepath}' (FORMAT PARQUET)
        """)
        con.close()

        # Remove the CSV.gz file to save space
        csv_gz_filepath.unlink()
        print(f"Completed {parquet_filename}")

def update_gitignore():
    gitignore_path = Path(".gitignore")

    # Read existing content or start with empty string
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    # Add data/ if not already present
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

@app.command()
def download_and_load(
    taxi_type: str,
    year: int
):
    """
    Docstring for download_and_load
    """
    # Update .gitignore to exclude data directory
    update_gitignore()

    download_and_convert_files(taxi_type, year)

    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    con.execute(f"""
        -- Step 1: Create table if not exists
        CREATE TABLE IF NOT EXISTS prod.{taxi_type}_tripdata AS
        SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        LIMIT 0;  -- creates empty table with schema only

        -- Step 2: Append data
        INSERT INTO prod.{taxi_type}_tripdata
        SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
    """)

    con.close()


if __name__ == "__main__":
    app()