from db_connect import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("✅ Connected! Tables:", tables)
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ DB connection failed:", e)
