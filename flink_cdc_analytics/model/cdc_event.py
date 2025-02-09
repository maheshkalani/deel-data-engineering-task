from pyflink.table import DataTypes
from pyflink.table.expressions import col

class CDCEvent:
    @staticmethod
    def get_schema(table_name):
        base_schema = [
            DataTypes.FIELD("before", DataTypes.ROW(CDCEvent.get_table_schema(table_name))),
            DataTypes.FIELD("after", DataTypes.ROW(CDCEvent.get_table_schema(table_name))),
            DataTypes.FIELD("op", DataTypes.STRING()),
            DataTypes.FIELD("ts_ms", DataTypes.BIGINT())
        ]
        return DataTypes.ROW(base_schema)

    @staticmethod
    def get_table_schema(table_name):
        if table_name == 'customers':
            return [
                DataTypes.FIELD("customer_id", DataTypes.BIGINT()),
                DataTypes.FIELD("customer_name", DataTypes.STRING()),
                DataTypes.FIELD("is_active", DataTypes.BOOLEAN()),
                DataTypes.FIELD("customer_address", DataTypes.STRING()),
                DataTypes.FIELD("updated_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("updated_by", DataTypes.BIGINT()),
                DataTypes.FIELD("created_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("created_by", DataTypes.BIGINT())
            ]
        elif table_name == 'products':
            return [
                DataTypes.FIELD("product_id", DataTypes.BIGINT()),
                DataTypes.FIELD("product_name", DataTypes.STRING()),
                DataTypes.FIELD("barcode", DataTypes.STRING()),
                DataTypes.FIELD("unity_price", DataTypes.DECIMAL(10, 2)),
                DataTypes.FIELD("is_active", DataTypes.BOOLEAN()),
                DataTypes.FIELD("updated_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("updated_by", DataTypes.BIGINT()),
                DataTypes.FIELD("created_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("created_by", DataTypes.BIGINT())
            ]
        elif table_name == 'orders':
            return [
                DataTypes.FIELD("order_id", DataTypes.BIGINT()),
                DataTypes.FIELD("order_date", DataTypes.DATE()),
                DataTypes.FIELD("delivery_date", DataTypes.DATE()),
                DataTypes.FIELD("customer_id", DataTypes.BIGINT()),
                DataTypes.FIELD("status", DataTypes.STRING()),
                DataTypes.FIELD("updated_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("updated_by", DataTypes.BIGINT()),
                DataTypes.FIELD("created_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("created_by", DataTypes.BIGINT())
            ]
        elif table_name == 'order_items':
            return [
                DataTypes.FIELD("order_item_id", DataTypes.BIGINT()),
                DataTypes.FIELD("order_id", DataTypes.BIGINT()),
                DataTypes.FIELD("product_id", DataTypes.BIGINT()),
                DataTypes.FIELD("quantity", DataTypes.INT()),
                DataTypes.FIELD("updated_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("updated_by", DataTypes.BIGINT()),
                DataTypes.FIELD("created_at", DataTypes.TIMESTAMP(3)),
                DataTypes.FIELD("created_by", DataTypes.BIGINT())
            ]
        else:
            raise ValueError(f"Unknown table: {table_name}")

    @staticmethod
    def get_latest_data(table):
        return table.select(
            col('after.*'),
            col('op').alias('operation'),
            col('ts_ms').alias('event_timestamp')
        ).where(col('op').is_not_null() & (col('op') != 'DELETE'))
