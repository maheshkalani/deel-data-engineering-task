# ACME Delivery Services Analytics Pipeline

This project implements a real-time analytics pipeline for ACME Delivery Services, processing order data from a transactional database and providing insights through a command-line interface.

## Prerequisites

- Docker and Docker Compose
- Git

## Setup and Installation

1. Clone the repository
2. Build and start the Docker containers:
```shell
    docker-compose up -d
````
This command will start the following services:

- Source PostgreSQL database
- Kafka and Zookeeper
- Debezium connector
- Flink JobManager and TaskManager
- cli tool
 
## Using the CLI Tool

The CLI tool allows you to export analytical results to CSV files. Use the following command structure:

```shell
docker-compose run --rm cli-tool --query <query_type> --output <output_file.csv>
```

Available query types:
- `open_orders`: Number of open orders by DELIVERY_DATE and STATUS
- `top_delivery_dates`: Top 3 delivery dates with more open orders
- `pending_items`: Number of open pending items by PRODUCT_ID
- `top_customers`: Top 3 Customers with more pending orders

Example:
```shell
docker-compose run --rm cli-tool --query open_orders --output /app/output/open_orders.csv
```
