from bronze.bronze_api_to_s3 import (
    run_bronze
)

from silver.silver_transform import (
    run_silver
)

from gold.gold_load_snowflake import (
    load_to_gold
)


def main():

    print(
        "\nPipeline Started\n"
    )

    run_bronze()

    cleaned_orders = (
        run_silver()
    )

    load_to_gold(
        cleaned_orders
    )

    print(
        "\nPipeline Completed\n"
    )


if __name__ == "__main__":
    main()