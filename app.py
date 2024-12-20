import sqlite3
import datetime
import re

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

def add_medication(brand_name, medication_name, expiry_date, location, notes=None):
    """Adds a new medication to the database."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medications (brand_name, medication_name, expiry_date, location, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (brand_name, medication_name, expiry_date, location, notes))
    conn.commit()
    conn.close()
    print("Medication added successfully.")

def view_medications(search_term=None):
    """Fetches and prints all medications in the database, optionally filtering by search term."""
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


def get_medication_by_id(medication_id):
    """Fetches a medication by its ID."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications WHERE medication_id = ?", (medication_id,))
    medication = cursor.fetchone()
    conn.close()
    return medication

def update_medication(medication_id, brand_name, medication_name, expiry_date, location, notes):
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
    """, (brand_name, medication_name, expiry_date, location, notes, medication_id))
    conn.commit()
    conn.close()
    print("Medication updated successfully.")

def delete_medication(medication_id):
    """Deletes a medication from the database."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE medication_id = ?", (medication_id,))
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
    add_medication(brand_name, medication_name, expiry_date_str, location, notes if notes else None)

def cli_edit_medication(medication_id = None):
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
    
    brand_name = input(f"Enter new brand name (leave empty to keep '{medication[1]}'): ") or medication[1]
    medication_name = input(f"Enter new medication name (leave empty to keep '{medication[2]}'): ") or medication[2]
    expiry_date_str = input(f"Enter new expiry date (YYYY/MM, leave empty to keep '{medication[3]}'): ") or medication[3]
    
    # Input validation for date format
    try:
        if expiry_date_str != medication[3]:
             datetime.datetime.strptime(expiry_date_str, "%Y/%m")
    except ValueError:
        print("Invalid date format. Please use YYYY/MM.")
        return
    
    location = input(f"Enter new location (leave empty to keep '{medication[4]}'): ") or medication[4]
    notes = input(f"Enter new notes (leave empty to keep '{medication[5] if medication[5] else ''}'): ")
    notes = notes if notes else (medication[5] if medication[5] else None)
   
    update_medication(medication_id, brand_name, medication_name, expiry_date_str, location, notes)


def cli_delete_medication():
    """Interactively prompts the user to delete a medication."""
    view_medications() # Display medications with IDs
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

    confirmation = input(f"Are you sure you want to delete {medication[2]}? (y/n): ")
    if confirmation.lower() == 'y':
        delete_medication(medication_id)
    else:
        print("Deletion cancelled.")

def get_closest_expiry():
    """Gets the medication with the closest expiry date."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()
    conn.close()
    
    closest_expiry = None
    closest_expiry_date = None
    
    for medication in medications:
      try:
        expiry_date = datetime.datetime.strptime(medication[3], "%Y/%m").date()
      except ValueError:
          continue
      
      if closest_expiry_date is None or expiry_date < closest_expiry_date:
          closest_expiry_date = expiry_date
          closest_expiry = medication
    
    return closest_expiry

def get_expired_medications():
    """Gets all medications that have expired today."""
    conn = sqlite3.connect("medications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()
    conn.close()

    today = datetime.date.today()
    expired_medications = []
    today_str = today.strftime("%Y/%m")  # Format today to YYYY/MM

    for medication in medications:
        try:
            if medication[3] == today_str:
                expired_medications.append(medication)
        except ValueError:
            continue
    
    return expired_medications

def main():
    create_database()
    
    while True:
        expired_medications = get_expired_medications()
        closest_expiry = get_closest_expiry()
    
        print("\nMedication Tracker Menu")
        
        if expired_medications:
          print("Alert: The following medications have expired today. Please edit or delete:")
          for med in expired_medications:
              print(f"   - ID:{med[0]}, Brand:{med[1]}, Med:{med[2]}, Expiry:{med[3]}")
        
          print("You must edit or delete these medications before adding new ones.")
            
        elif closest_expiry:
           print("Alert: The following medication has the soonest expiry date:")
           print(f"  ID: {closest_expiry[0]}")
           print(f"  Brand Name: {closest_expiry[1]}")
           print(f"  Medication Name: {closest_expiry[2]}")
           print(f"  Expiry Date: {closest_expiry[3]}")
           print("---")
        else:
          print("No medications found or no valid expiry dates.")

        print("1. Add Medication")
        print("2. View Medications")
        print("3. Edit Medication")
        print("4. Delete Medication")
        print("5. Search Medications")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if expired_medications and choice == "1":
          print("You must edit or delete expired medications before adding new ones.")
        elif choice == "1":
            cli_add_medication()
        elif choice == "2":
            view_medications()
        elif choice == "3":
            if expired_medications:
              med_id_str = input("Enter the ID of the expired medication to edit: ")
              try:
                  med_id = int(med_id_str)
                  # Check if medication_id is in expired_medications
                  if any(med[0] == med_id for med in expired_medications):
                      cli_edit_medication(med_id)
                      expired_medications = get_expired_medications()  # Refresh the expired list after editing.
                  else:
                      print("Invalid medication ID for expired medications.")
              except ValueError:
                 print("Invalid medication ID.")
            else:
                cli_edit_medication()
        elif choice == "4":
            cli_delete_medication()
        elif choice =="5":
           search_term = input("Enter your search term: ")
           view_medications(search_term)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()