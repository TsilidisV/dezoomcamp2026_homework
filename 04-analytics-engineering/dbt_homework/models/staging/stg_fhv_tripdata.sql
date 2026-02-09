select
    -- identifiers
    cast(Affiliated_base_number as varchar(6)) as affiliated_base_number,
    cast(dispatching_base_num as varchar(6)) as dispatching_base_num,

    -- trip info
    cast(DOlocationID as integer) as pickup_location_id,
    cast(DOlocationID as integer) as dropoff_location_id,
    cast(pickup_datetime as timestamp) as pickup_datetime, 
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    cast(SR_Flag as int) as sr_flag,

from {{ source('raw_data', 'fhv_tripdata') }}

-- filter out records with null vendor_id (data quality requirement)
where dispatching_base_num is not null