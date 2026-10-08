"""
database/load_to_mysql.py
-------------------------
Loads cleaned commute data into MySQL database 'mumbai_commute_db'.
Useful for college viva demonstration of Database connectivity.
"""

import os
import pandas as pd
import mysql.connector

def load_data_to_mysql(host="localhost", user="root", password="", database="mumbai_commute_db"):
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "commute_data_cleaned.csv")
    if not os.path.exists(csv_path):
        print("Cleaned CSV not found! Please run data_processing.py first.")
        return

    df = pd.read_csv(csv_path)

    try:
        print(f"Connecting to MySQL server at {host} as user '{user}'...")
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Create database and table if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commute_data (
                Commute_ID VARCHAR(20) PRIMARY KEY,
                Date DATE NOT NULL,
                Starting_Area VARCHAR(50) NOT NULL,
                Destination VARCHAR(50) NOT NULL,
                Transport_Mode VARCHAR(20) NOT NULL,
                Distance_km DECIMAL(5,2) NOT NULL,
                Travel_Time_min INT NOT NULL,
                Waiting_Time_min INT NOT NULL,
                Cost_INR INT NOT NULL,
                Peak_Hour VARCHAR(5) NOT NULL,
                Crowd_Level VARCHAR(20) NOT NULL,
                Delay_min INT NOT NULL,
                Weather VARCHAR(20) NOT NULL,
                Comfort_Rating INT NOT NULL,
                User_Rating INT NOT NULL,
                Total_Trip_Time_min INT,
                Cost_Per_Km DECIMAL(6,2),
                Speed_kmh DECIMAL(5,2)
            )
        """)

        # Clear existing rows to prevent duplicate primary keys
        cursor.execute("TRUNCATE TABLE commute_data")

        # Insert rows
        insert_query = """
            INSERT INTO commute_data (
                Commute_ID, Date, Starting_Area, Destination, Transport_Mode,
                Distance_km, Travel_Time_min, Waiting_Time_min, Cost_INR,
                Peak_Hour, Crowd_Level, Delay_min, Weather, Comfort_Rating,
                User_Rating, Total_Trip_Time_min, Cost_Per_Km, Speed_kmh
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        records = [tuple(x) for x in df.to_numpy()]
        cursor.executemany(insert_query, records)
        conn.commit()

        print(f"Successfully inserted {cursor.rowcount} records into MySQL table '{database}.commute_data'!")
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("\n[MySQL Notice]")
        print(f"Could not connect to MySQL server: {err}")
        print("If you are running MySQL (e.g. XAMPP / MySQL Workbench):")
        print("1. Ensure MySQL service is running.")
        print("2. Check your MySQL password in this script.")
        print("Note: The Flask application and Data Science pipeline work independently using the CSV.")

if __name__ == "__main__":
    load_data_to_mysql()

