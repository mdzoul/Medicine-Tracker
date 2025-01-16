"""
This script is to be run first. Prior to running the script:
1. Ensure that the CSV file (e.g. `client_data.csv`) is located in the project folder.
2. The CSV file should have the following columns: "Brand", "Medication Name", "Expiry Date", "Location".

This script will:
1. Create an SQLite database file called `medications.db` in the project folder.
2. Create a `medications` table with the following columns: `brand_name`, `medication_name`, `expiry_date`, `location`.
3. Read the CSV file and insert the data into the `medications` table.

Once the script has been run, the database will be set up and populated with the data from the CSV.
"""

import csv
import os
import sqlite3
import sys

# Ensure the CSV file exists in the project folder
CSV_FILENAME = "BCExpiryStock.csv"  # Ensure the file name matches the actual file

if not os.path.exists(CSV_FILENAME):
    print(
        f"Error: {CSV_FILENAME} not found. Please ensure the file is in the project folder."
    )
    sys.exit(1)

try:
    # Connect to SQLite (this will create the database file if it doesn't exist)
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()

    # Create the medications table if it doesn't already exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS medications (
            medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL,
            medication_name TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            location TEXT,
            notes TEXT
        )
    """
    )

    # Open the CSV file and read data into the database
    with open(CSV_FILENAME, "r") as file:
        reader = csv.DictReader(
            file
        )  # Read CSV into a dictionary format (column names as keys)

        # Check if the CSV file is empty
        rows = list(reader)
        if not rows:
            print("Error: The CSV file is empty.")
            sys.exit(1)

        # Debug: Print the first row to check the CSV reading
        print(f"First row in CSV: {rows[0]}")

        for row in rows:
            try:
                # Map CSV columns to database columns
                brand_name = row["Brand"]
                medication_name = row["Name"]
                expiry_date = row["Expiry"]
                location = row["Location"]
                notes = row["Notes"]

                # Insert data into the database
                cursor.execute(
                    """
                    INSERT INTO medications (brand_name, medication_name, expiry_date, location, notes)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (brand_name, medication_name, expiry_date, location, notes),
                )

            except KeyError as e:
                print(f"Error: Missing expected column in the CSV file - {e}")
                sys.exit(1)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print(
        "Database `medications.db` created and populated successfully with data from the CSV."
    )

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    sys.exit(1)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
