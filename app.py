import datetime
import re
import sqlite3

from dateutil.relativedelta import relativedelta
from flask import Flask, redirect, render_template, request, url_for

from database import MedicationDatabase

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change for a very complex key


def get_expiry_alerts(db):
    """Gets medications with the closest expiry date, within one month, and within two months."""
    with db as db_conn:
        db_conn.cursor.execute("SELECT * FROM medications")
        medications = db_conn.cursor.fetchall()

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
            closest_expiry_meds = [medication]  # new min date, reset list
        elif expiry_date == closest_expiry_date:
            closest_expiry_meds.append(medication)  # same min date, append to the list

    return {
        "expired": expired_meds,
        "expiring_in_one_month": expiring_in_one_month_meds,
        "expiring_in_two_months": expiring_in_two_months_meds,
        "closest_expiry": closest_expiry_meds,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    db = MedicationDatabase()
    expiry_alerts = get_expiry_alerts(db)
    brand_name_error = None

    if request.method == "POST":
        brand_name = request.form.get("brand_name")
        medication_name = request.form.get("medication_name")
        expiry_date = request.form.get("expiry_date")
        location = request.form.get("location")
        notes = request.form.get("notes")

        with db as db_conn:
            db_conn.cursor.execute(
                "SELECT * FROM medications WHERE brand_name = ?", (brand_name,)
            )
            existing_med = db_conn.cursor.fetchone()
            if existing_med:
                brand_name_error = "A medication with this brand name already exists"
            else:
                db.add_medication(
                    brand_name,
                    medication_name,
                    expiry_date,
                    location,
                    notes if notes else None,
                )
                return redirect(url_for("index"))

    return render_template(
        "index.html", expiry_alerts=expiry_alerts, brand_name_error=brand_name_error
    )


@app.route("/medications", methods=["GET"])
def medications():
    db = MedicationDatabase()
    search_term = request.args.get("search_term", "")
    sort_by = request.args.get("sort_by", "medication_id")
    sort_order = request.args.get("sort_order", "asc")

    with db as db_conn:
        query = "SELECT * FROM medications"
        query_args = []

        if search_term:
            query += (
                " WHERE brand_name LIKE ? OR medication_name LIKE ? OR location LIKE ?"
            )
            query_args.extend(
                [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
            )

        query += f" ORDER BY {sort_by} {sort_order}"

        db_conn.cursor.execute(query, query_args)
        medications = db_conn.cursor.fetchall()

    expiry_alerts = get_expiry_alerts(db)

    return render_template(
        "medications.html",
        medications=medications,
        sort_by=sort_by,
        search_term=search_term,
        sort_order=sort_order,
        expiry_alerts=expiry_alerts,
    )


@app.route("/edit/<int:medication_id>", methods=["GET", "POST"])
def edit_medication(medication_id):
    db = MedicationDatabase()
    medication = db.get_medication_by_id(medication_id)
    if not medication:
        return "Medication not found", 404

    if request.method == "POST":
        brand_name = request.form.get("brand_name")
        medication_name = request.form.get("medication_name")
        expiry_date = request.form.get("expiry_date")
        location = request.form.get("location")
        notes = request.form.get("notes")
        db.update_medication(
            medication_id,
            brand_name,
            medication_name,
            expiry_date,
            location,
            notes if notes else None,
        )
        return redirect(
            url_for("index")
        )  # redirect to the index once you have finished

    expiry_alerts = get_expiry_alerts(db)
    return render_template(
        "index.html", medication=medication, expiry_alerts=expiry_alerts
    )


if __name__ == "__main__":
    app.run(debug=True)
