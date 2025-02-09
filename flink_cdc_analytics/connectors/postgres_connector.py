# src/main/python/connectors/postgres_connector.py

from pyflink.table import TableDescriptor, Schema
from flink_cdc_analytics.config.job_config import POSTGRES_JDBC_URL, POSTGRES_USERNAME, POSTGRES_PASSWORD

class PostgresConnector:
    @staticmethod
    def create_sink_table(t_env, table_name, schema):
        """
        Create a temporary table in Flink that maps to a PostgreSQL table.
        """
        t_env.create_temporary_table(
            f'postgres_sink_{table_name}',
            TableDescriptor.for_connector('jdbc')
            .schema(Schema.new_builder()
                    .from_schema(schema)
                    .build())
            .option('connector', 'jdbc')
            .option('url', POSTGRES_JDBC_URL)
            .option('table-name', table_name)
            .option('username', POSTGRES_USERNAME)
            .option('password', POSTGRES_PASSWORD)
            .option('sink.upsert-mode', 'true')
            .build()
        )

    @staticmethod
    def create_analytics_tables(t_env):
        """
        Create PostgreSQL tables for analytical results with primary keys.
        These tables will support upserts.
        """
        # Open orders by delivery date and status
        t_env.execute_sql("""
            CREATE TABLE IF NOT EXISTS open_orders_by_delivery_date_and_status (
                delivery_date DATE,
                status STRING,
                open_order_count BIGINT,
                PRIMARY KEY (delivery_date, status) NOT ENFORCED
            ) WITH (
                'connector' = 'jdbc',
                'url' = '{}',
                'table-name' = 'open_orders_by_delivery_date_and_status',
                'username' = '{}',
                'password' = '{}'
            )
        """.format(POSTGRES_JDBC_URL, POSTGRES_USERNAME, POSTGRES_PASSWORD))

        # Top delivery dates
        t_env.execute_sql("""
            CREATE TABLE IF NOT EXISTS top_delivery_dates (
                delivery_date DATE,
                open_order_count BIGINT,
                PRIMARY KEY (delivery_date) NOT ENFORCED
            ) WITH (
                'connector' = 'jdbc',
                'url' = '{}',
                'table-name' = 'top_delivery_dates',
                'username' = '{}',
                'password' = '{}'
            )
        """.format(POSTGRES_JDBC_URL, POSTGRES_USERNAME, POSTGRES_PASSWORD))

        # Pending items by product
        t_env.execute_sql("""
            CREATE TABLE IF NOT EXISTS pending_items_by_product (
                product_id BIGINT,
                pending_item_count BIGINT,
                PRIMARY KEY (product_id) NOT ENFORCED
            ) WITH (
                'connector' = 'jdbc',
                'url' = '{}',
                'table-name' = 'pending_items_by_product',
                'username' = '{}',
                'password' = '{}'
            )
        """.format(POSTGRES_JDBC_URL, POSTGRES_USERNAME, POSTGRES_PASSWORD))

        # Top customers with pending orders
        t_env.execute_sql("""
            CREATE TABLE IF NOT EXISTS top_customers_with_pending_orders (
                customer_id BIGINT,
                pending_order_count BIGINT,
                PRIMARY KEY (customer_id) NOT ENFORCED
            ) WITH (
                'connector' = 'jdbc',
                'url' = '{}',
                'table-name' = 'top_customers_with_pending_orders',
                'username' = '{}',
                'password' = '{}'
            )
        """.format(POSTGRES_JDBC_URL, POSTGRES_USERNAME, POSTGRES_PASSWORD))
