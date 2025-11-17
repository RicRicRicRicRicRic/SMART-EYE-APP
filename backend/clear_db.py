import sqlite3
import os

DATABASE = 'smart_eye.db'
TABLES_TO_CLEAR = ['drone_logs', 'drone_status']

def clear_all_data():
    if not os.path.exists(DATABASE):
        print(f"Database file '{DATABASE}' not found in this directory.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        print("\n--- Database Cleaning Starting ---")
        
        for table in TABLES_TO_CLEAR:
            try:
                cursor.execute(f"DELETE FROM {table}")
                
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                rows_remaining = cursor.fetchone()[0]
                
                print(f"Table '{table}' cleared. Rows remaining: {rows_remaining}")
            except sqlite3.OperationalError:
                print(f"Warning: Table '{table}' not found or could not be accessed. Skipping.")

        conn.commit()
        print(f"--- Database Cleaning Successful ---")
        
    except sqlite3.OperationalError as e:
        print(f"ERROR: Could not access the database.")
        print(f"Detail: {e}")
        print("ACTION: Ensure the 'backend.py' server is STOPPED before running this script.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    clear_all_data()