import sqlite3

def free_database(cursor):
    cursor.execute("DELETE FROM other_data")
    cursor.execute("DELETE FROM product")
    print("Database freed successfully")