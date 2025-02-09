from pyflink.table import Table
from pyflink.table.expressions import col, lit

class Analytics:
    @staticmethod
    def open_orders_by_delivery_date_and_status(orders_table: Table) -> Table:
        return orders_table.filter(col('status').in_(['Open', 'Pending'])) \
            .group_by(col('delivery_date'), col('status')) \
            .select(col('delivery_date'), col('status'), col('order_id').count.alias('open_order_count'))

    @staticmethod
    def top_delivery_dates(orders_table: Table) -> Table:
        return orders_table.filter(col('status').in_(['Open', 'Pending'])) \
            .group_by(col('delivery_date')) \
            .select(col('delivery_date'), col('order_id').count.alias('open_order_count')) \
            .order_by(col('open_order_count').desc) \
            .limit(3)

    @staticmethod
    def pending_items_by_product(orders_table: Table, order_items_table: Table) -> Table:
        return orders_table.join(order_items_table, col('orders.order_id') == col('order_items.order_id')) \
            .filter(col('status').in_(['Open', 'Pending'])) \
            .group_by(col('product_id')) \
            .select(col('product_id'), col('quantity').sum.alias('pending_item_count'))

    @staticmethod
    def top_customers_with_pending_orders(orders_table: Table) -> Table:
        # First, calculate pending orders for all customers
        all_customers = orders_table.filter(col('status').in_(['Open', 'Pending'])) \
            .group_by(col('customer_id')) \
            .select(
            col('customer_id'),
            col('order_id').count.alias('pending_order_count')
        )

        third_highest = all_customers \
            .select(col('pending_order_count')) \
            .order_by(col('pending_order_count').desc) \
            .offset(2).limit(1)

        return all_customers.join(third_highest, how='cross') \
            .where(col('pending_order_count') >= col('pending_order_count').r) \
            .select(
            col('customer_id'),
            col('pending_order_count'),
            lit(1).count.over(
                order_by=col('pending_order_count').desc,
                partition_by=[]
            ).alias('rank')
        )
