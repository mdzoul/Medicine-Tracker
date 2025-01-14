"""
This module provides a class to handle all interactions with
the medication database.
It uses SQLite to store and retrieve medication information.
The class provides methods to create the database, add, view, edit,
and delete medication records.
"""

import re
import sqlite3


class MedicationDatabase:
    """Handles all database interactions."""

    def __init__(self, db_name="medications.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_database(self):
        """Creates the database and the medications table if they don't exist."""
        with self as db:
            db.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS medications (
                    medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand_name TEXT NOT NULL,
                    medication_name TEXT NOT NULL,
                    expiry_date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    notes TEXT
                )
            """
            )
            db.conn.commit()
            print("Database created/connected.")

    def add_medication(
        self, brand_name, medication_name, expiry_date, location, notes=None
    ):
        """Adds a new medication to the database."""
        with self as db:
            db.cursor.execute(
                """
                INSERT INTO medications (brand_name, medication_name, expiry_date, location, notes)
                VALUES (?, ?, ?, ?, ?)
             """,
                (brand_name, medication_name, expiry_date, location, notes),
            )
            db.conn.commit()
            print("Medication added successfully.")

    def view_medications(self, search_term=None):
        """Fetches and prints all medications in the database, optionally filtering by search term."""
        with self as db:
            db.cursor.execute("SELECT * FROM medications")
            medications = db.cursor.fetchall()

        if not medications:
            print("No medications found in the database.")
            return None

        if search_term:
            print(f"Search results for '{search_term}':\n")
            found_meds = False
            regex = re.compile(re.escape(search_term), re.IGNORECASE)
            for medication in medications:
                brand_name = medication[1]
                medication_name = medication[2]

                if regex.search(brand_name) or regex.search(medication_name):
                    print(f"ID: {medication[0]}")
                    print(f"Brand Name: {medication[1]}")
                    print(f"Medication Name: {medication[2]}")
                    print(f"Expiry Date: {medication[3]}")
                    print(f"Location: {medication[4]}")
                    print(f"Notes: {medication[5] if medication[5] else 'No notes'}")
                    print("---")
                    found_meds = True
            if not found_meds:
                print("No matching medications found.")
        else:
            print("List of medications:\n")
            for medication in medications:
                print(f"ID: {medication[0]}")
                print(f"Brand Name: {medication[1]}")
                print(f"Medication Name: {medication[2]}")
                print(f"Expiry Date: {medication[3]}")
                print(f"Location: {medication[4]}")
                print(f"Notes: {medication[5] if medication[5] else 'No notes'}")
                print("---")
        return medications

    def get_medication_by_id(self, medication_id):
        """Fetches a medication by its ID."""
        with self as db:
            db.cursor.execute(
                "SELECT * FROM medications WHERE medication_id = ?", (medication_id,)
            )
            medication = db.cursor.fetchone()
            return medication

    def update_medication(
        self, medication_id, brand_name, medication_name, expiry_date, location, notes
    ):
        """Updates an existing medication in the database."""
        with self as db:
            db.cursor.execute(
                """
                UPDATE medications
                SET brand_name = ?,
                    medication_name = ?,
                    expiry_date = ?,
                    location = ?,
                    notes = ?
                WHERE medication_id = ?
            """,
                (
                    brand_name,
                    medication_name,
                    expiry_date,
                    location,
                    notes,
                    medication_id,
                ),
            )
            db.conn.commit()
            print("Medication updated successfully.")

    def delete_medication(self, medication_id):
        """Deletes a medication from the database."""
        with self as db:
            db.cursor.execute(
                "DELETE FROM medications WHERE medication_id = ?", (medication_id,)
            )
            db.conn.commit()
            print("Medication deleted successfully.")
