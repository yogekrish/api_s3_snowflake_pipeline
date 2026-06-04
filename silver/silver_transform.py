import json

from config.config import (
    S3_BUCKET_NAME,
    BRONZE_KEY,
    SILVER_KEY
)

from utils.s3_client import (
    get_s3_client
)


def read_bronze_data():

    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=S3_BUCKET_NAME,
        Key=BRONZE_KEY
    )

    content = (
        response["Body"]
        .read()
        .decode("utf-8")
    )

    return json.loads(content)


def get_customer_tier(total_amount):

    if total_amount >= 1000:
        return "Premium"

    elif total_amount >= 500:
        return "Gold"

    elif total_amount >= 100:
        return "Silver"

    return "Regular"


def is_valid_email(email):

    return (
        "@" in email and
        "." in email
    )


def safe_int(value):

    try:
        return int(value)

    except:
        return None


def safe_float(value):

    try:
        return float(value)

    except:
        return None


def transform_data(raw_orders):

    cleaned_orders = []

    for order in raw_orders:

        raw_order_id = order.get("order_id")

        if raw_order_id is None:
            continue

        order_id = str(raw_order_id).strip()

        if not order_id.isdigit():
            continue

        customer_name = str(
            order.get("customer_name", "")
        ).strip()

        email = str(
            order.get("email", "")
        ).strip().lower()

        quantity = safe_int(
            order.get("quantity")
        )

        unit_price = safe_float(
            order.get("unit_price")
        )

        if (
            order_id == "" or
            customer_name == "" or
            not is_valid_email(email) or
            quantity is None or
            unit_price is None
        ):
            continue

        total_amount = (
            quantity *
            unit_price
        )

        transformed_record = {

            "order_id":
                int(order_id),

            "customer_name":
                customer_name.title(),

            "email":
                email,

            "email_domain":
                email.split("@")[1],

            "product":
                str(
                    order.get(
                        "product",
                        ""
                    )
                ).strip().title(),

            "category":
                str(
                    order.get(
                        "category",
                        ""
                    )
                ).strip().title(),

            "quantity":
                quantity,

            "unit_price":
                unit_price,

            "total_amount":
                total_amount,

            "country":
                str(
                    order.get(
                        "country",
                        ""
                    )
                ).strip().title(),

            "customer_tier":
                get_customer_tier(
                    total_amount
                )
        }

        cleaned_orders.append(
            transformed_record
        )

    return cleaned_orders


def write_silver_data(cleaned_orders):

    s3 = get_s3_client()

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=SILVER_KEY,
        Body=json.dumps(
            cleaned_orders,
            indent=4
        ),
        ContentType="application/json"
    )

    print("Silver Layer Loaded")


def run_silver():

    raw_data = read_bronze_data()

    cleaned_orders = transform_data(
        raw_data
    )

    write_silver_data(
        cleaned_orders
    )

    return cleaned_orders