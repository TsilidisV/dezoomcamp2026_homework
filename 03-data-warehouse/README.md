
# Module 3 Homework


This project demonstrates a Data Engineering platform using **Terraform** for Infrastructure as Code (IaC) and **Kestra** for orchestration. It automatically provisions a Google Cloud Storage bucket and deploys a Kestra flow to ingest NYC Taxi data into it.

## 📂 Project Structure

```text
.
├── docker-compose.yml       # Kestra services (Postgres + Kestra)
├── Makefile                 # Automation commands
├── infrastructure/          # Terraform GCP resources
│   ├── main.tf
│   ├── outputs.tf
│   └── keys/                # Place your GCP Service Account JSON here
└── orchestration/           # Kestra Flow definitions
    └── _flows/
        ├── batch_runner.yml
        └── data_ingest.yml

```

## 🛠️ Prerequisites

1. **Docker & Docker Compose** installed and running.
2. **Terraform** installed.
3. **Google Cloud Service Account Key**:
* Create a Service Account in GCP with `Storage Admin` permissions.
* Download the JSON key.
* Save it as: `./infrastructure/keys/service-account.json`

## 🚀 Quick Start

Use the included `Makefile` to automate the entire setup.

Simply run
```bash
make demo
```

or manually follow these steps:

### 1. Provision Infrastructure

Initialize Terraform, create the GCS bucket, and generate the `.env` file for Kestra.

```bash
make infra-up
```

### 2. Start Kestra

Launch Kestra and its database.

```bash
make kestra-up
```

*Access the UI at: [http://localhost:8080*](https://www.google.com/search?q=http://localhost:8080)
*(Login: `admin@kestra.io` / `Admin1234`)*

### 3. Run the Pipeline

You can trigger the flows directly from the Kestra UI:

1. Go to **Flows** -> `batch-runner`.
2. Click **New Execution**.
3. This will trigger the `data-ingest` subflow for multiple months.

## 🧹 Clean Up

To destroy the GCP resources (bucket) and stop the containers:

```bash
make infra-down
```

## 📝 Configuration

* **Secrets:** GCP credentials are automatically encoded and passed to Kestra via `SECRET_GCP_CREDS` in the `.env` file.
* **Hot Reload:** The `./orchestration/_flows` directory is mounted to the container. Edits to YAML files are reflected instantly.

## Module 3 Homework

<b><u>Important Note:</b></u> <p> For this homework we will be using the Yellow Taxi Trip Records for **January 2024 - June 2024 NOT the entire year of data** 
Parquet Files from the New York
City Taxi Data found here: </br> https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page </br>
If you are using orchestration such as Kestra, Mage, Airflow or Prefect etc. do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>



<b>BIG QUERY SETUP:</b></br>
Create an external table using the Yellow Taxi Trip Records. </br>
Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table). </br>
</p>

<details>
  <summary>Click to show solution</summary>

```SQL
-- External table creation
CREATE OR REPLACE EXTERNAL TABLE dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external
OPTIONS (
  format = 'Parquet',
  uris = ["gs://homework_3_bucket_chum/yellow_tripdata_2024-*"]
);


-- Regular table creation
CREATE OR REPLACE TABLE dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024
AS SELECT * FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external;
```

</details>

## Question 1:
What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093 ✅
- 85,431,289


<details>
  <summary>Click to show solution</summary>

```SQL
SELECT COUNT(VendorID)
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external
```

</details>

## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table ✅
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

<details>
  <summary>Click to show solution</summary>

```SQL
SELECT COUNT(DISTINCT PULocationID) AS number_of_disinct_PULocationIDs
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external

SELECT COUNT(DISTINCT PULocationID) AS number_of_disinct_PULocationIDs
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024
```

</details>

## Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed. ✅
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, 
doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

<details>
  <summary>Click to show solution</summary>

```SQL
SELECT PULocationID
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024

SELECT PULocationID, DOLocationID
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024
```

</details>

## Question 4:
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333 ✅

<details>
  <summary>Click to show solution</summary>

```SQL
SELECT fare_amount, COUNT(fare_amount) as fare_amount_count
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external
WHERE fare_amount = 0
GROUP BY fare_amount
```

</details>

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID ✅
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

<details>
  <summary>Click to show solution</summary>

```SQL
CREATE OR REPLACE TABLE dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_partitioned_clustered
PARTITION BY
  DATE(tpep_dropoff_datetime)
CLUSTER BY
  VendorID 
AS SELECT * FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_external;
```

</details>

## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table ✅
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

<details>
  <summary>Click to show solution</summary>

```SQL
SELECT DISTINCT VendorID
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM dezoomcamp-2026.homework_3_dataset.yellow_tripdata_2024_partitioned_clustered
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

</details>

## Question 7: 
Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- GCP Bucket ✅
- Big Table


## Question 8:
It is best practice in Big Query to always cluster your data:
- True
- False ✅



## (Bonus: Not worth points) Question 9:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?


<details>
  <summary>Click to show solution</summary>

Because BigQuery stores metadata for every materialized table. Running `SELECT count(*)` for a materialized table has BigQuery just look at the table's metadata.

</details>
