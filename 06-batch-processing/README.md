# Module 6 Homework

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2025-11 data from the official website:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```

Additionally, I'll use the following dockerfile which installs python, java 21, pyspark 4.1 and jupyterlab 4.0.9 for ease of use:

```dockerfile
# 1. Use a lightweight Python base image
FROM python:3.12-slim

# 2. Set environment variables
# This prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# This prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# 3. Install OpenJDK-21 (Required for PySpark)
# We use 'slim' images, so we need to install Java manually.
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# 5. Install PySpark and JupyterLab
# We specify versions to ensure compatibility
RUN pip install --no-cache-dir \
    pyspark==4.1.0 \
    jupyterlab==4.0.9

# 6. Set the working directory
WORKDIR /workspace

# 7. Expose the Jupyter port
EXPOSE 8888

# 8. Start JupyterLab
# --ip=0.0.0.0 makes it accessible from outside the container
# --no-browser prevents trying to open a browser inside the container
# --allow-root allows running as root user
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

```yaml
services:
  pyspark-notebook:
    build: .
    container_name: my-pyspark-jupyter
    ports:
      - "8888:8888"  # Jupyter Lab Port
      - "4040:4040"  # Spark Master Web UI Port
    volumes:
      # Maps the local 'work' folder to the container's notebook directory
      # This ensures your work is saved even if the container stops
      - ./work:/workspace
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?



<details>
  <summary>Click to show solution</summary>

The output is "4.1.0" which can be seen by running the following code:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Production ETL Job") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

print(f"Spark Version: {spark.version}")
```

</details>


## Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB ✅
- 75MB 
- 100MB

<details>
  <summary>Click to show solution</summary>

The four parquet files created are about 24,982MB, 24,982MB, 25,003MB, and 25,003MB, hence they are about 25MB. We execute the following code to download the data and repartition them in spark.

```python
from urllib.request import urlretrieve

# Download the data
url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet'
file = './data/yellow_tripdata_2025-11.parquet'
urlretrieve(url, file)

# Read the data as a spark dataframe
df = spark.read.parquet(file)

# Repartition and save the data
repartitioned_path = './data/repartitioned/'
df.repartition(4).write \
    .mode("overwrite") \
    .parquet(repartitioned_path)
```
</details>

## Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- 162,604 ✅
- 225,768

<details>
  <summary>Click to show solution</summary>

```python
import pyspark.sql.functions as F

dfre = spark.read.parquet(repartitioned_path)

dfre \
    .select() \
    .filter(F.to_date(F.col('tpep_pickup_datetime')) == '2025-11-15') \
    .count()
```
</details>

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- 90.6 ✅
- 134.5

<details>
  <summary>Click to show solution</summary>
We'll use spark's `timestamp_diff` function and then the `max` function.

```python
dfre \
    .withColumn('DiffInHours', F.timestamp_diff('minute', 'tpep_pickup_datetime', 'tpep_dropoff_datetime') / 60 ) \
    .select(F.max('DiffInHours')) \
    .show(truncate=False)
```
</details>



## Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040 ✅
- 8080

<details>
  <summary>Click to show solution</summary>
It's 4040 and that's why we have

```yaml
...
    ports:
      - "8888:8888"  # Jupyter Lab Port
      - "4040:4040"  # Spark Master Web UI Port
...
```
in the docker compose, i.e, we map the port 4040 inside the Docker container to our local port 4040. Then, we can access Spark' UI by visiting http://localhost:4040/jobs/.

</details>


## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island ✅
- Arden Heights ✅
- Rikers Island
- Jamaica Bay

If multiple answers are correct, select any

<details>
  <summary>Click to show solution</summary>
  
There's also the zone "Governor's Island/Ellis Island/Liberty Island" which is missing from the answers. To get the results, we run the following code.

```python
from urllib.request import urlretrieve

url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
zone_file = './data/taxi_zone_lookup.csv'
urlretrieve(url, zone_file)

# 2. Read the zone lookup data
df_zones = spark.read \
    .option("header", "true") \
    .csv(zone_file)

df_zones.createOrReplaceTempView('zones')
dfre.createOrReplaceTempView('trips')

spark.sql("""
    SELECT 
        z.Zone, 
        COUNT(*) as trip_count
    FROM trips AS t
    INNER JOIN zones AS z
        ON t.PULocationID = z.LocationID
    GROUP BY 
        z.Zone
    ORDER BY trip_count ASC
""").show(truncate=False)
```

with the zones with least trips being:
```
+---------------------------------------------+----------+
|Zone                                         |trip_count|
+---------------------------------------------+----------+
|Eltingville/Annadale/Prince's Bay            |1         |
|Governor's Island/Ellis Island/Liberty Island|1         |
|Arden Heights                                |1         |

```

</details>