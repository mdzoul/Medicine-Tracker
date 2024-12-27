import sqlite3
import datetime
from dateutil.relativedelta import relativedelta
import asyncio
from database import MedicationDatabase
from notifier import TelegramNotifier


def main():
    db = MedicationDatabase()
    notifier = TelegramNotifier()

    def send_alerts():
        """Sends all the Telegram alerts"""
        expiry_alerts = get_expiry_alerts()

        # Run the async function
        asyncio.run(notifier.send_telegram_alert(expiry_alerts))

    def get_expiry_alerts():
        """ Gets medications with the closest expiry date, within one month, and within two months"""
        conn = sqlite3.connect(db.db_name)
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

    send_alerts()


if __name__ == "__main__":
    main()
