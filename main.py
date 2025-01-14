import asyncio

from app import MedicationTrackerApp

if __name__ == "__main__":
    app = MedicationTrackerApp()
    asyncio.run(app.run())
