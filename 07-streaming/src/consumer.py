import sys
from datetime import datetime
from pathlib import Path

from models import Ride, ride_deserializer

import psycopg2
from kafka import KafkaConsumer

server = 'localhost:9092'
topic_name = 'green-trips'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5433,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-to-postgres',
    value_deserializer=ride_deserializer
)

cur.execute("""
    CREATE TABLE IF NOT EXISTS processed_events (
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    passenger_count DOUBLE PRECISION,
    trip_distance DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    total_amount DOUBLE PRECISION
    )
""")

print(f"Listening to {topic_name} and writing to PostgreSQL...")

count = 0
for message in consumer:
    ride = message.value
    
    pickup_dt = datetime.strptime(ride.lpep_pickup_datetime, '%Y-%m-%d %H:%M:%S')
    lpep_dropoff_dt = datetime.strptime(ride.lpep_dropoff_datetime, '%Y-%m-%d %H:%M:%S')
    
    cur.execute(
        """INSERT INTO processed_events
           (lpep_pickup_datetime, lpep_dropoff_datetime, PULocationID, DOLocationID, passenger_count, trip_distance, tip_amount, total_amount)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (pickup_dt, lpep_dropoff_dt, ride.PULocationID, ride.DOLocationID, ride.passenger_count, ride.trip_distance, ride.tip_amount, ride.total_amount)
    )
    count += 1
    if count % 100 == 0:
        print(f"Inserted {count} rows...")

consumer.close()
cur.close()
conn.close()