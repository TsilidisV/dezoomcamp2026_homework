import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text
import pandas as pd

def main():
    load_dotenv()  # This loads the .env file
    
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    host = os.getenv('HOST')
    port = os.getenv('PORT')

     # We get the variable here
    db_url =  f"postgresql+psycopg2://{db_user}:{db_password}@{host}:{port}/{db_name}"
    
    df_green_taxi = pd.read_parquet("https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet", engine="pyarrow")

    engine = create_engine(db_url)

    df_green_taxi.head(0).to_sql(name='green_taxi', con=engine, if_exists='replace', index=False)
    df_green_taxi.to_sql(name='green_taxi', con=engine, if_exists='append', index=False, chunksize=10000, method='multi')

    # Create table schema only from an empty DataFrame
    CSV_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    TABLE_NAME = 'time_zone'
    dtype_map = { 'LocationID': Integer(), 'Borough': Text(), 'Zone': Text(), 'service_zone': Text() } 
    df_time_zones = pd.read_csv(CSV_URL, nrows=0)
    df_time_zones.to_sql(name=TABLE_NAME, con=engine, if_exists="replace", index=False, dtype=dtype_map)

    # Stream the CSV in chunks and append
    chunksize = 10_000
    for chunk in pd.read_csv(CSV_URL, chunksize=chunksize):
        chunk.to_sql(name=TABLE_NAME, con=engine, if_exists="append", index=False, method="multi")


if __name__ == "__main__":
    main()
