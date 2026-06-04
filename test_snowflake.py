from utils.snowflake_client import get_snowflake_connection

conn = get_snowflake_connection()
cursor = conn.cursor()

cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")

print("Snowflake connected successfully")
print(cursor.fetchone())

cursor.close()
conn.close()