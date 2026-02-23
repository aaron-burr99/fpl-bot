import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST') 
DB_USER = os.getenv('DB_USER') 
DB_PASSWORD = os.getenv('DB_PASSWORD') 
DB_NAME = os.getenv('DB_NAME') 
TABLE_NAME = os.getenv('TABLE_NAME') 

def create_database_and_table():
    try:
        # 1. Connect to the MySQL server (without specifying a database initially)
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD
        )
        cursor = conn.cursor()

        # 2. Create the database
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print(f"Database '{DB_NAME}' already exists.")
            else:
                print(err.msg)
                return
        
        # 3. Reconnect to use the newly created (or existing) database
        # This is a common practice, alternatively you can use the `database` parameter in the initial connect
        conn.close() 
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # 4. Create the table with 'name' (VARCHAR) and 'score' (INT)
        # Added a primary key 'id' for better database practices
        create_table_query = f"""
        CREATE TABLE {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            score INT
        )
        """
        try:
            cursor.execute(create_table_query)
            print(f"Table '{TABLE_NAME}' created successfully with 'name' and 'score' columns.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Table '{TABLE_NAME}' already exists.")
            else:
                print(err.msg)

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
    finally:
        # 5. Close the connection and cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None and conn.is_connected():
            conn.close()
            print("MySQL connection closed.")

def update_table(data_dict):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        for name, score in data_dict.items():
            # Check if the name already exists in the table
            cursor.execute(f"SELECT id FROM {TABLE_NAME} WHERE name = %s", (name,))
            result = cursor.fetchone()

            if result:
                # Name exists — overwrite the score
                cursor.execute(
                    f"UPDATE {TABLE_NAME} SET score = %s WHERE name = %s",
                    (score, name)
                )
                print(f"Updated score for '{name}' to {score}.")
            else:
                # Name doesn't exist — insert a new entry
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (name, score) VALUES (%s, %s)",
                    (name, score)
                )
                print(f"Inserted new entry for '{name}' with score {score}.")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None and conn.is_connected():
            conn.close()
            print("MySQL connection closed.")

def get_table():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT name, score FROM {TABLE_NAME}")
        rows = cursor.fetchall()

        scores_dict = {name: score for name, score in rows}
        return scores_dict

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None and conn.is_connected():
            conn.close()
            
if __name__ == "__main__":
    create_database_and_table()
