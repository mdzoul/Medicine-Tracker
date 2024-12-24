import sqlite3
import datetime
import re
from dateutil.relativedelta import relativedelta


def create_database():
    """Creates the database and the medications table if they don't exist."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL,
            medication_name TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            location TEXT NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database created/connected.")


def add_medication(
        brand_name,
        medication_name,
        expiry_date,
        location,
        notes=None
        ):
    """Adds a new medication to the database."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medications (
            brand_name,
            medication_name,
            expiry_date,
            location,
            notes)
        VALUES (?, ?, ?, ?, ?)
    """, (brand_name, medication_name, expiry_date, location, notes))
    conn.commit()
    conn.close()
    print("Medication added successfully.")


def view_medications(search_term=None):
    """Fetches and prints all medications in the database,
    optionally filtering by search term."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()
    conn.close()

    if not medications:
        print("No medications found in the database.")
        return

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
                print(f"Notes: {
                    medication[5] if medication[5] else 'No notes'
                    }")
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


def get_medication_by_id(medication_id):
    """Fetches a medication by its ID."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute(
            "SELECT * FROM medications WHERE medication_id = ?",
            (medication_id,)
            )
    medication = cursor.fetchone()
    conn.close()
    return medication


def update_medication(
        medication_id,
        brand_name,
        medication_name,
        expiry_date,
        location,
        notes
        ):
    """Updates an existing medication in the database."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE medications
        SET brand_name = ?,
            medication_name = ?,
            expiry_date = ?,
            location = ?,
            notes = ?
        WHERE medication_id = ?
    """, (
        brand_name,
        medication_name,
        expiry_date,
        location,
        notes,
        medication_id
        )
                   )
    conn.commit()
    conn.close()
    print("Medication updated successfully.")


def delete_medication(medication_id):
    """Deletes a medication from the database."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE medication_id = ?",
                   (medication_id,))
    conn.commit()
    conn.close()
    print("Medication deleted successfully.")


def cli_add_medication():
    """Interactively prompts the user to add a new medication."""
    brand_name = input("Enter brand name: ")
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
    add_medication(
            brand_name,
            medication_name,
            expiry_date_str,
            location,
            notes if notes else None
            )


def cli_edit_medication(medication_id=None, expired_medications=None):
    """Interactively prompts the user to edit an existing medication."""

    if medication_id is None:
        view_medications()  # Show medications with their IDs first
        medication_id = input("Enter the ID of the medication to edit: ")
        try:
            medication_id = int(medication_id)
        except ValueError:
            print("Invalid medication ID.")
            return

    medication = get_medication_by_id(medication_id)
    if not medication:
        print("Medication not found.")
        return

    print("Current medication details:")
    print(f"  Brand Name: {medication[1]}")
    print(f"  Medication Name: {medication[2]}")
    print(f"  Expiry Date: {medication[3]}")
    print(f"  Location: {medication[4]}")
    print(f"  Notes: {medication[5] if medication[5] else 'No notes'}")

    brand_name = input("Enter new brand name (leave empty to keep "
                       f"'{medication[1]}'): ") or medication[1]
    medication_name = input("Enter new medication name (leave empty to keep "
                            f"'{medication[2]}'): ") or medication[2]
    expiry_date_str = input("Enter new expiry date (YYYY/MM, leave empty to keep "
                            f"'{medication[3]}'): ") or medication[3]

    # Input validation for date format
    try:
        if expiry_date_str != medication[3]:
            datetime.datetime.strptime(expiry_date_str, "%Y/%m")
    except ValueError:
        print("Invalid date format. Please use YYYY/MM.")
        return

    location = input("Enter new location (leave empty to keep "
                     f"'{medication[4]}'): ") or medication[4]
    notes = input("Enter new notes (leave empty to keep "
                  f"'{medication[5] if medication[5] else ''}'): ")
    notes = notes if notes else (medication[5] if medication[5] else None)

    update_medication(
            medication_id,
            brand_name,
            medication_name,
            expiry_date_str,
            location,
            notes
            )


def cli_delete_medication():
    """Interactively prompts the user to delete a medication."""
    view_medications()  # Display medications with IDs
    medication_id = input("Enter the ID of the medication to delete: ")
    try:
        medication_id = int(medication_id)
    except ValueError:
        print("Invalid medication ID.")
        return

    medication = get_medication_by_id(medication_id)
    if not medication:
        print("Medication not found.")
        return

    confirmation = input("Are you sure you want to delete "
                         f"{medication[2]}? (y/n): ")
    if confirmation.lower() == 'y':
        delete_medication(medication_id)
    else:
        print("Deletion cancelled.")


def get_expiry_alerts():
    """Gets medications with the closest expiry date,
    within one month, and within two months."""
    conn = sqlite3.connect("medications.db")
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
            expiry_date = datetime.datetime.strptime(medication[3],
                                                     "%Y/%m").date()
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
            closest_expiry_meds.append(medication)

    return {
        "expired": expired_meds,
        "expiring_in_one_month": expiring_in_one_month_meds,
        "expiring_in_two_months": expiring_in_two_months_meds,
        "closest_expiry": closest_expiry_meds
    }


def display_alerts(expiry_alerts):
    """Displays the alerts."""
    if expiry_alerts["expired"]:
        print("Alert: The following medications have expired today. "
              "Please edit or delete:")
        for med in expiry_alerts["expired"]:
            print(f"   - ID:{med[0]}, "
                  f"Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}")
        print("You must edit or delete these medications "
              "before adding new ones.")
        print("-----------------------")

    if expiry_alerts["expiring_in_one_month"]:
        print("Alert: "
              "The following medication(s) expire within the next month:")
        for med in expiry_alerts["expiring_in_one_month"]:
            print(f"   - ID:{med[0]}, "
                  f"Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}")

    if expiry_alerts["expiring_in_two_months"]:
        print("Alert: "
              "The following medication(s) expire within the next two months:")
        for med in expiry_alerts["expiring_in_two_months"]:
            print(f"   - ID:{med[0]}, "
                  f"Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}")

    if expiry_alerts["closest_expiry"] and not expiry_alerts["expiring_in_one_month"] and not expiry_alerts["expiring_in_two_months"]:
        print("Alert: "
              "The following medication(s) have the soonest expiry date:")
        for med in expiry_alerts["closest_expiry"]:
            print(f"   - ID:{med[0]}, "
                  f"Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}")

    if not expiry_alerts["expired"] and not expiry_alerts["expiring_in_one_month"] and not expiry_alerts["expiring_in_two_months"] and not expiry_alerts["closest_expiry"]:
        print("No medications found or no valid expiry dates.")


def handle_add_medication(expiry_alerts):
    """Handles the add medication logic."""
    if expiry_alerts["expired"]:
        print("You must edit or delete expired medications "
              "before adding new ones.")
    else:
        cli_add_medication()


def handle_edit_medication(expiry_alerts):
    """Handles the edit medication logic"""
    if expiry_alerts["expired"]:
        med_id_str = input("Enter the ID of the expired medication to edit: ")
        try:
            med_id = int(med_id_str)
            # Check if medication_id is in expired_medications
            if any(med[0] == med_id for med in expiry_alerts["expired"]):
                cli_edit_medication(med_id, expiry_alerts["expired"])
            else:
                print("Invalid medication ID for expired medications.")
        except ValueError:
            print("Invalid medication ID.")
    else:
        cli_edit_medication()


def main():
    create_database()

    while True:
        expiry_alerts = get_expiry_alerts()

        print("\nMedication Tracker Menu")
        print("-----------------------")
        display_alerts(expiry_alerts)

        print("-----------------------")
        print("1. Add Medication")
        print("2. View Medications")
        print("3. Edit Medication")
        print("4. Delete Medication")
        print("5. Search Medications")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            handle_add_medication(expiry_alerts)
        elif choice == "2":
            view_medications()
        elif choice == "3":
            handle_edit_medication(expiry_alerts)
        elif choice == "4":
            cli_delete_medication()
        elif choice == "5":
            search_term = input("Enter your search term: ")
            view_medications(search_term)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
