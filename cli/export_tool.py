import click
import psycopg2
import csv
from psycopg2.extras import RealDictCursor

@click.command()
@click.option('--query', type=click.Choice(['open_orders', 'top_delivery_dates', 'pending_items', 'top_customers']))
@click.option('--output', type=click.Path(writable=True))
def export_to_csv(query, output):
    conn = psycopg2.connect("dbname=analytics_db user=finance_db_user password=1234 host=localhost:5432")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if query == 'open_orders':
        cur.execute("SELECT * FROM open_orders_by_delivery_date_and_status")
    elif query == 'top_delivery_dates':
        cur.execute("SELECT * FROM top_delivery_dates")
    elif query == 'pending_items':
        cur.execute("SELECT * FROM pending_items_by_product")
    elif query == 'top_customers':
        cur.execute("SELECT * FROM top_customers_with_pending_orders")

    results = cur.fetchall()

    with open(output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    click.echo(f"Results exported to {output}")

    cur.close()
    conn.close()

if __name__ == '__main__':
    export_to_csv()
