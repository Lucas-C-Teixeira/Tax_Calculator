# database/setup_db.py
import sqlite3
import os

def init_database():
    # Get the absolute path of the directory where THIS script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths relative to this script's directory
    schema_path = os.path.join(current_dir, "schema.sql")
    db_path = os.path.join(current_dir, "taxes.db")

    if not os.path.exists(schema_path):
        print(f"Error: Could not find {schema_path}")
        return

    try:
        # Connect (this will create taxes.db inside the database folder)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        with open(schema_path, "r") as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        connection.commit()
        connection.close()

        print(f"Successfully created database at: {db_path}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

if __name__ == "__main__":
    init_database()