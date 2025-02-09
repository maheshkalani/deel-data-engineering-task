from pyflink.table import TableDescriptor, Schema
from flink_cdc_analytics.model.cdc_event import CDCEvent
from flink_cdc_analytics.config.job_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPICS

class KafkaConnector:
    @staticmethod
    def create_source_table(t_env, table_name):
        return t_env.create_temporary_table(
            f'kafka_source_{table_name}',
            TableDescriptor.for_connector('kafka')
            .schema(Schema.new_builder()
                    .column('event', CDCEvent.get_schema(table_name))
                    .build())
            .option('connector', 'kafka')
            .option('topic', KAFKA_TOPICS[table_name])
            .option('properties.bootstrap.servers', KAFKA_BOOTSTRAP_SERVERS)
            .option('properties.group.id', KAFKA_CONSUMER_GROUP)
            .option('format', 'json')
            .option('json.fail-on-missing-field', 'false')
            .option('json.ignore-parse-errors', 'true')
            .build()
        )

    @staticmethod
    def get_latest_data(t_env, table_name):
        source_table = t_env.from_path(f'kafka_source_{table_name}')
        return CDCEvent.get_latest_data(source_table)
