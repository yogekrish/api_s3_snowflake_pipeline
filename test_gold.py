# test_gold.py

from silver.silver_transform import run_silver
from gold.gold_load_snowflake import load_to_gold

cleaned_orders = run_silver()
load_to_gold(cleaned_orders)