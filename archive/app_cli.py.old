"""
This module manages the core application logic for the Medication Tracker CLI.
It sets up the database connection, manages user interactions, displays alerts,
and handles the command line interface.
"""

import datetime
import sqlite3

from dateutil.relativedelta import relativedelta

from database import MedicationDatabase


class MedicationTrackerApp:
    """Manages the UI and orchestrates app logic."""

    def __init__(self):
        self.db = MedicationDatabase()

    def cli_add_medication(self):
        """Interactively prompts the user to add a new medication."""
        brand_name = input("Enter brand name: ")

        # Check if brand name already exists
        with self.db as db:
            db.cursor.execute(
                "SELECT * FROM medications WHERE brand_name = ?", (brand_name,)
            )
            existing_meds = db.cursor.fetchall()

        if existing_meds:
            print(
                "Warning: A medication with the same brand name already exists. Details:"
            )
            for medication in existing_meds:
                print(
                    f"   - ID:{medication[0]}, Brand:{medication[1]}, Med:{medication[2]}, Expiry:{medication[3]}"
                )

            confirmation = input("Do you still want to continue? (y/n): ")
            if confirmation.lower() != "y":
                print("Addition cancelled.")
                return

        medication_name = input("Enter medication name: ")
        expiry_date_str = input("Enter expiry date (YYYY/MM): ")

        # Input validation for date format
        try:
            datetime.datetime.strptime(expiry_date_str, "%Y/%m")
        except ValueError:
            print("Invalid date format. Please use YYYY/MM.")
            return

        location = input("Enter location: ")
        notes = input("Enter notes (optional, press Enter to skip): ")
        self.db.add_medication(
            brand_name,
            medication_name,
            expiry_date_str,
            location,
            notes if notes else None,
        )

    def cli_edit_medication(self, medication_id=None, expired_medications=None):
        """Interactively prompts the user to edit an existing medication."""

        if medication_id is None:
            self.db.view_medications()  # Show medications with their IDs first
            medication_id = input("Enter the ID of the medication to edit: ")
            try:
                medication_id = int(medication_id)
            except ValueError:
                print("Invalid medication ID.")
                return

        medication = self.db.get_medication_by_id(medication_id)
        if not medication:
            print("Medication not found.")
            return

        print("Current medication details:")
        print(f"  Brand Name: {medication[1]}")
        print(f"  Medication Name: {medication[2]}")
        print(f"  Expiry Date: {medication[3]}")
        print(f"  Location: {medication[4]}")
        print(f"  Notes: {medication[5] if medication[5] else 'No notes'}")

        brand_name = (
            input(f"Enter new brand name (leave empty to keep '{medication[1]}'): ")
            or medication[1]
        )
        medication_name = (
            input(
                f"Enter new medication name (leave empty to keep '{medication[2]}'): "
            )
            or medication[2]
        )
        expiry_date_str = (
            input(
                f"Enter new expiry date (YYYY/MM, leave empty to keep '{medication[3]}'): "
            )
            or medication[3]
        )

        # Input validation for date format
        try:
            if expiry_date_str != medication[3]:
                datetime.datetime.strptime(expiry_date_str, "%Y/%m")
        except ValueError:
            print("Invalid date format. Please use YYYY/MM.")
            return

        location = (
            input(f"Enter new location (leave empty to keep '{medication[4]}'): ")
            or medication[4]
        )
        notes = input(
            f"Enter new notes (leave empty to keep '{
                      medication[5] if medication[5] else ''}'): "
        )
        notes = notes if notes else (medication[5] if medication[5] else None)

        self.db.update_medication(
            medication_id, brand_name, medication_name, expiry_date_str, location, notes
        )

    def cli_delete_medication(self):
        """Interactively prompts the user to delete a medication."""
        self.db.view_medications()
        medication_id = input("Enter the ID of the medication to delete: ")
        try:
            medication_id = int(medication_id)
        except ValueError:
            print("Invalid medication ID.")
            return

        medication = self.db.get_medication_by_id(medication_id)
        if not medication:
            print("Medication not found.")
            return

        confirmation = input(
            f"Are you sure you want to delete {medication[2]}? (y/n): "
        )
        if confirmation.lower() == "y":
            self.db.delete_medication(medication_id)
        else:
            print("Deletion cancelled.")

    def get_expiry_alerts(self):
        """Gets medications with the closest expiry date,
        within one month, and within two months."""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medications")
        medications = cursor.fetchall()
        conn.close()

        today = datetime.date.today()
        one_month_later = today + relativedelta(months=1)
        two_months_later = today + relativedelta(months=2)

        expired_meds = []
        expiring_in_one_month_meds = []
        expiring_in_two_months_meds = []
        closest_expiry_meds = []
        closest_expiry_date = None

        for medication in medications:
            try:
                expiry_date = datetime.datetime.strptime(medication[3], "%Y/%m").date()
            except ValueError:
                continue

            if expiry_date <= today:
                expired_meds.append(medication)
            elif today < expiry_date <= one_month_later:
                expiring_in_one_month_meds.append(medication)
            elif today < expiry_date <= two_months_later:
                expiring_in_two_months_meds.append(medication)

            if closest_expiry_date is None or expiry_date < closest_expiry_date:
                closest_expiry_date = expiry_date
                closest_expiry_meds = [medication]
            elif expiry_date == closest_expiry_date:
                # same min date, append to the list
                closest_expiry_meds.append(medication)

        return {
            "expired": expired_meds,
            "expiring_in_one_month": expiring_in_one_month_meds,
            "expiring_in_two_months": expiring_in_two_months_meds,
            "closest_expiry": closest_expiry_meds,
        }

    def display_alerts(self, expiry_alerts):
        """Displays the alerts."""
        if expiry_alerts["expired"]:
            print(
                "Alert: The following medications have expired today. Please edit or delete:"
            )
            for med in expiry_alerts["expired"]:
                print(
                    f"   - ID:{med[0]}, Brand:{med[1]
                                                 }, Med:{med[2]}, Expiry:{med[3]}"
                )
            print("You must edit or delete these medications before adding new ones.")

        if expiry_alerts["expiring_in_one_month"]:
            print("Alert: The following medication(s) expire within the next month:")
            for med in expiry_alerts["expiring_in_one_month"]:
                print(
                    f"   - ID:{med[0]}, Brand:{med[1]
                                                 }, Med:{med[2]}, Expiry:{med[3]}"
                )

        if expiry_alerts["expiring_in_two_months"]:
            print(
                "Alert: The following medication(s) expire within the next two months:"
            )
            for med in expiry_alerts["expiring_in_two_months"]:
                print(
                    f"   - ID:{med[0]}, Brand:{med[1]
                                                 }, Med:{med[2]}, Expiry:{med[3]}"
                )

        if (
            expiry_alerts["closest_expiry"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
        ):
            print("Alert: The following medication(s) have the soonest expiry date:")
            for med in expiry_alerts["closest_expiry"]:
                print(
                    f"   - ID:{med[0]}, Brand:{med[1]
                                                 }, Med:{med[2]}, Expiry:{med[3]}"
                )

        if (
            not expiry_alerts["expired"]
            and not expiry_alerts["expiring_in_one_month"]
            and not expiry_alerts["expiring_in_two_months"]
            and not expiry_alerts["closest_expiry"]
        ):
            print("No medications found or no valid expiry dates.")

    def handle_add_medication(self, expiry_alerts):
        """Handles the add medication logic."""
        if expiry_alerts["expired"]:
            print(
                "You must edit or delete expired medications " "before adding new ones."
            )
        else:
            self.cli_add_medication()

    def handle_edit_medication(self, expiry_alerts):
        """Handles the edit medication logic"""
        if expiry_alerts["expired"]:
            med_id_str = input("Enter the ID of the expired medication to edit: ")
            try:
                med_id = int(med_id_str)
                if any(med[0] == med_id for med in expiry_alerts["expired"]):
                    self.cli_edit_medication(med_id, expiry_alerts["expired"])
                else:
                    print("Invalid medication ID for expired medications.")
            except ValueError:
                print("Invalid medication ID.")
        else:
            self.cli_edit_medication()

    def run(self):
        self.db.create_database()
        while True:
            expiry_alerts = self.get_expiry_alerts()

            print("\nMedication Tracker Menu")
            self.display_alerts(expiry_alerts)

            print("1. Add Medication")
            print("2. View Medications")
            print("3. Edit Medication")
            print("4. Delete Medication")
            print("5. Search Medications")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.handle_add_medication(expiry_alerts)
            elif choice == "2":
                self.db.view_medications()
            elif choice == "3":
                self.handle_edit_medication(expiry_alerts)
            elif choice == "4":
                self.cli_delete_medication()
            elif choice == "5":
                search_term = input("Enter your search term: ")
                self.db.view_medications(search_term)
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = MedicationTrackerApp()
    app.run()
