CREATE TABLE clicks(
    click_id STRING,
    user_id INT,
    product_id STRING,
    product STRING,
    price DOUBLE,
    url STRING,
    user_agent STRING,
    ip_address STRING,
    datetime_occured TIMESTAMP(3),
    processing_time as PROCTIME(),
    WATERMARK for datetime_occured - INTERVAL '15' SECOND
) WITH (
    'connector'='{{connector}}',
    'topic'='{{topic}}',
    'properties.bootstrap.server'='{{bootstrap_servers}}',
    'propertis.group_id'='{{consumer_group_id}}',
    'scan.startup,mode'='{{scan_startup_mode}}',
    'format'='{{format}}'
);