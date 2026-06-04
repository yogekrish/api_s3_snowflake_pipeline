from config.config import (
    GOLD_TABLE
)

from utils.snowflake_client import (
    get_snowflake_connection
)


def create_gold_table(cursor):

    query = f"""
    CREATE TABLE IF NOT EXISTS
    {GOLD_TABLE}
    (
        order_id INTEGER,
        customer_name STRING,
        email STRING,
        email_domain STRING,
        product STRING,
        category STRING,
        quantity INTEGER,
        unit_price FLOAT,
        total_amount FLOAT,
        country STRING,
        customer_tier STRING
    )
    """

    cursor.execute(query)


def load_to_gold(cleaned_orders):

    conn = get_snowflake_connection()

    cursor = conn.cursor()

    create_gold_table(cursor)

    insert_query = f"""
    INSERT INTO {GOLD_TABLE}
    (
        order_id,
        customer_name,
        email,
        email_domain,
        product,
        category,
        quantity,
        unit_price,
        total_amount,
        country,
        customer_tier
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s
    )
    """

    rows = []

    for order in cleaned_orders:

        rows.append(
            (
                order["order_id"],
                order["customer_name"],
                order["email"],
                order["email_domain"],
                order["product"],
                order["category"],
                order["quantity"],
                order["unit_price"],
                order["total_amount"],
                order["country"],
                order["customer_tier"]
            )
        )

    cursor.executemany(
        insert_query,
        rows
    )

    conn.commit()

    cursor.close()
    conn.close()

    print(
        "Gold Layer Loaded"
    )