KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_CONSUMER_GROUP = 'flink-cdc-analytics'

KAFKA_TOPICS = {
    'customers': 'debezium.transactions_db_cdc.operations.customers',
    'products': 'debezium.transactions_db_cdc.operations.products',
    'orders': 'debezium.transactions_db_cdc.operations_orders',
    'order_items': 'debezium.transactions_db_cdc.operations_order_items'
}

POSTGRES_JDBC_URL = 'jdbc:postgresql://localhost:5432/analytics_db'
POSTGRES_USERNAME = 'cdc_user'
POSTGRES_PASSWORD = 'cdc_1234'

FLINK_CHECKPOINT_INTERVAL = 60000  # milliseconds
FLINK_CHECKPOINT_PATH = 'file:///path/to/checkpoints'
