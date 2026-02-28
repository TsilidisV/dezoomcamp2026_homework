# Module 5 Homework: Data Platforms with Bruin

In this homework, we'll use Bruin to build a complete data pipeline, from ingestion to reporting.

## Setup

1. Install Bruin CLI: `curl -LsSf https://getbruin.com/install/cli | sh`
2. Initialize the zoomcamp template: `bruin init zoomcamp my-pipeline`
3. Configure your `.bruin.yml` with a DuckDB connection
4. Follow the tutorial in the [main module README](../../../05-data-platforms/)

After completing the setup, you should have a working NYC taxi data pipeline.

---

### Question 1. Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere) ✅
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

<details>
  <summary>Click to show solution</summary>
  
A Bruin project primarily requires a connection configuration file (`.bruin.yml`) and a pipeline definition file (`pipeline.yml`). While the `assets/` directory is the conventional location for defining pipeline assets (SQL, Python, etc.), the pipeline structure is flexible enough that assets can be located elsewhere as long as they are correctly referenced or discovered.
</details>

---

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column ✅
- `view` - create a virtual table only

<details>
  <summary>Click to show solution</summary>
  
The `time_interval` materialization strategy is designed specifically for incremental processing based on a time column. It allows you to process data for a specific time period (e.g., a specific month) by deleting existing records in that interval and inserting the new ones. This ensures idempotency for time-partitioned data.

- `append` would create duplicates if run multiple times for the same period.
- `replace` would delete the entire table, not just the specific interval.
- `view` does not store data physically.
</details>

---

### Question 3. Pipeline Variables

You have the following variable defined in `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'` ✅
- `bruin run --set taxi_types=["yellow"]`

<details>
  <summary>Click to show solution</summary>
  
To override an array variable defined in `pipeline.yml`, you must pass a JSON-compatible array string to the `--var` flag. 

`bruin run --var 'taxi_types=["yellow"]'` correctly passes an array containing a single string element "yellow".

Passing `taxi_types=yellow` (without brackets) would typically be interpreted as a string, not an array, which might cause type mismatch errors depending on how the variable is used in the pipeline.
</details>

---

### Question 4. Running with Dependencies

You've modified the `ingestion/trips.py` asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream` ✅
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

<details>
  <summary>Click to show solution</summary>
  
The Bruin CLI provides specific flags for handling dependencies. The `--downstream` flag is used to run the specified asset and all assets that depend on it (downstream).

`bruin run ingestion/trips.py --downstream` targets the specific file and includes all downstream effects.

(Note: While some tools like dbt use selector graph operators like `+`, Bruin utilizes explicit flags like `--downstream` and `--upstream` for this functionality).
</details>

---

### Question 5. Quality Checks

You want to ensure the `pickup_datetime` column in your trips table never has NULL values. Which quality check should you add to your asset definition?

- `name: unique`
- `name: not_null` ✅
- `name: positive`
- `name: accepted_values, value: [not_null]`

<details>
  <summary>Click to show solution</summary>
  
The `not_null` check is the standard quality check for ensuring that a column does not contain any NULL values. It is a fundamental data integrity constraint used in most data transformation tools.

- `unique` ensures all values are distinct.
- `positive` checks for numeric values greater than zero.
- `accepted_values` checks if values belong to a specific list.
</details>

---

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage` ✅
- `bruin show`

<details>
  <summary>Click to show solution</summary>
  
The `bruin lineage` command is designed to parse your pipeline assets and visualize the dependency graph. It typically outputs a visual representation (like a Mermaid diagram) showing how assets connect, helping you understand the flow of data through your pipeline.
</details>

---

### Question 7. First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

- `--create`
- `--init`
- `--full-refresh` ✅
- `--truncate`

<details>
  <summary>Click to show solution</summary>
  
The `--full-refresh` flag is the standard way to ensure that assets are rebuilt from scratch. 

While a first-time run naturally creates tables, `--full-refresh` is the explicit flag used to drop existing tables (or incremental state) and recreate them. This is crucial for incremental models to ensure they initialize correctly without adhering to previous state boundaries, or if you need to reset your environment.

- `--create` and `--init` are not standard Bruin run flags.
- `--truncate` is not a top-level flag; truncation is a behavior managed by the materialization strategy or the full-refresh flag.
</details>

---