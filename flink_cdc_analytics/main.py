from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from connectors.kafka_connector import KafkaConnector
from connectors.postgres_connector import PostgresConnector
from transformations.analytics import Analytics

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Create Kafka source tables
    KafkaConnector.create_source_table(t_env, "orders")
    KafkaConnector.create_source_table(t_env, "order_items")

    # Create PostgreSQL sink tables (with upsert support)
    PostgresConnector.create_analytics_tables(t_env)

    # Perform analytics
    orders_table = KafkaConnector.get_latest_data(t_env, "orders")
    order_items_table = KafkaConnector.get_latest_data(t_env, "order_items")

    open_orders_result = Analytics.open_orders_by_delivery_date_and_status(orders_table)
    open_orders_result.execute_insert("open_orders_by_delivery_date_and_status")

    top_delivery_dates_result = Analytics.top_delivery_dates(orders_table)
    top_delivery_dates_result.execute_insert("top_delivery_dates")

    pending_items_result = Analytics.pending_items_by_product(orders_table, order_items_table)
    pending_items_result.execute_insert("pending_items_by_product")

    top_customers_result = Analytics.top_customers_with_pending_orders(orders_table)
    top_customers_result.execute_insert("top_customers_with_pending_orders")

    env.execute("Flink CDC Analytics Job")

if __name__ == "__main__":
    main()
