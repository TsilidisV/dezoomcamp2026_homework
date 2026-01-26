# Module 1 Homework: Docker & SQL

## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

- 25.3 ✅
- 24.3.1
- 24.2.1
- 23.3.1

<details open>
  <summary>Click to show solution</summary>

  ```bash
  docker run -it --rm --entrypoint=bash python:3.13
  ```

  ```bash
  pip --version
  > pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
  ```
</details>


## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432 ✅

<details open>
  <summary>Click to show solution</summary>

  We will connect inside of the container so service name is `db` and port is `5432`.
</details>


## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- 8,007 ✅
- 8,254
- 8,421

<details open>
  <summary>Click to show solution</summary>

  ```SQL
  SELECT COUNT(*) AS trips_le_1_mile
  FROM green_taxi
  WHERE lpep_pickup_datetime >= '2025-11-01'
    AND lpep_pickup_datetime <  '2025-12-01'
    AND trip_distance <= 1;
  ```
</details>

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- 2025-11-14 ✅
- 2025-11-20
- 2025-11-23
- 2025-11-25

<details open>
  <summary>Click to show solution</summary>

  ```SQL
  SELECT DATE(lpep_pickup_datetime) AS "pick up day with the longest trip distance"
  FROM green_taxi
  WHERE trip_distance <= 100
  ORDER BY trip_distance DESC
  LIMIT 1
  ```
</details>


## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North ✅
- East Harlem South
- Morningside Heights
- Forest Hills

<details open>
  <summary>Click to show solution</summary>

  ```SQL
  SELECT t."Zone", SUM(g.total_amount) as sum_total_amount
  FROM green_taxi as g
  INNER JOIN time_zone as t
    ON g."PULocationID" = t."LocationID"
  WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
  GROUP BY t."Zone"
  ORDER BY sum_total_amount DESC
  LIMIT 1
  ```
</details>

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West ✅
- East Harlem North
- LaGuardia Airport

<details open>
  <summary>Click to show solution</summary>

  ```SQL
  SELECT tdo."Zone" as "dropp off location", g.tip_amount
  FROM green_taxi AS g
  INNER JOIN time_zone as tpu
    ON tpu."LocationID" = g."PULocationID"
  INNER JOIN time_zone as tdo
    ON tdo."LocationID" = g."DOLocationID"
  WHERE tpu."Zone" = 'East Harlem North'
  ORDER BY g.tip_amount DESC
  LIMIT 1
  ```
</details>


## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy ✅
- terraform import, terraform apply -y, terraform rm
