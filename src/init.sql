CREATE SCHEMA IF NOT EXISTS `meliproject-452420.chromecast_ml`;

CREATE TABLE IF NOT EXISTS `meliproject-452420.chromecast_ml.sellers` (
    seller_id INT64 NOT NULL,
    name STRING NOT NULL,
    state STRING,
    city STRING,
    PRIMARY KEY (seller_id) NOT ENFORCED
);


CREATE TABLE IF NOT EXISTS `meliproject-452420.chromecast_ml.products` (
    product_id STRING NOT NULL,
    seller_id INT64 NOT NULL,
    title STRING NOT NULL,
    price FLOAT64 NOT NULL,
    available_quantity INT64,
    condition STRING,
    brand STRING,
    model STRING,
    PRIMARY KEY (product_id) NOT ENFORCED,
    FOREIGN KEY (seller_id) REFERENCES chromecast_ml.sellers(seller_id) NOT ENFORCED
);


CREATE TABLE IF NOT EXISTS `meliproject-452420.chromecast_ml.shipments` (
    shipping_id INT64 NOT NULL,
    product_id STRING NOT NULL,
    store_pick_up BOOL,
    free_shipping BOOL,
    logistic_type STRING,
    PRIMARY KEY (shipping_id) NOT ENFORCED,
    FOREIGN KEY (product_id) REFERENCES chromecast_ml.products(product_id) NOT ENFORCED
);