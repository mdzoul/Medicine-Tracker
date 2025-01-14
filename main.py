"""
This module is the main entry point for the Medication Tracker application.
It initializes and runs the MedicationTrackerApp, which orchestrates the
application's core logic.
"""

from app import MedicationTrackerApp

if __name__ == "__main__":
    app = MedicationTrackerApp()
    app.run()
