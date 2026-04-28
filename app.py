"""
Sugar Management System — Flask Backend
---------------------------------------
Handles routing and database interactions.
Business logic is imported from logic.py for clean separation.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

# Import business logic
import logic

# ─── App Configuration ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = "sugar_mgmt_secret_2024"

# Using a fresh database name to ensure schema integrity
DB_PATH = os.path.join(BASE_DIR, "database.db")

# ─── Database Helpers ─────────────────────────────────────────────────────────

def get_db():
    """Create a database connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema if it doesn't exist."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS farmers_data (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name         TEXT    NOT NULL,
                crop_type           TEXT    NOT NULL,
                soil_type           TEXT    NOT NULL,
                land_area           REAL    NOT NULL,
                irrigation_interval INTEGER NOT NULL,
                fertilizer_used     TEXT    NOT NULL,
                fertilizer_cost     REAL    NOT NULL,
                date_of_planting    TEXT    NOT NULL,
                water_usage         REAL    NOT NULL,
                yield_tons          REAL    NOT NULL,
                sugar_output_kg     REAL    NOT NULL,
                harvest_date        TEXT    NOT NULL,
                created_at          TEXT    NOT NULL
            )
        """)
    
    # Ensure DB file is writable
    try:
        os.chmod(DB_PATH, 0o666)
    except Exception:
        pass

# Always ensure DB is initialized on module load
init_db()

# ─── Context Processor ────────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {"now": datetime.now()}


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    """Render the main farm entry form."""
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Handle form submission, perform calculations via logic.py, and save to DB."""
    try:
        # 1. Extraction & Basic Validation
        farmer_name         = request.form.get("farmer_name", "").strip()
        crop_type           = request.form.get("crop_type", "").strip()
        soil_type           = request.form.get("soil_type", "").strip()
        land_area_raw       = request.form.get("land_area", "").strip()
        irrigation_int_raw  = request.form.get("irrigation_interval", "").strip()
        fertilizer_used     = request.form.get("fertilizer_used", "").strip()
        fert_cost_raw       = request.form.get("fertilizer_cost", "").strip()
        date_of_planting    = request.form.get("date_of_planting", "").strip()

        if not all([farmer_name, crop_type, soil_type, land_area_raw,
                    irrigation_int_raw, fertilizer_used, fert_cost_raw, date_of_planting]):
            flash("⚠ All fields are required to perform calculations.", "error")
            return redirect(url_for("home"))

        # 2. Type Conversion
        land_area           = float(land_area_raw)
        irrigation_interval = int(irrigation_int_raw)
        fertilizer_cost     = float(fert_cost_raw)

        # 3. Domain Validation
        if land_area <= 0:
            flash("⚠ Land area must be a positive value.", "error")
            return redirect(url_for("home"))
        if fertilizer_cost < 0:
            flash("⚠ Fertilizer cost cannot be negative.", "error")
            return redirect(url_for("home"))

        # 4. Calculations (Pure Logic)
        planting_date   = datetime.strptime(date_of_planting, "%Y-%m-%d")
        water_usage     = logic.calculate_water(land_area, irrigation_interval)
        yield_tons      = logic.estimate_yield(land_area, soil_type, crop_type)
        sugar_output_kg = logic.calculate_sugar_output(yield_tons, crop_type)
        harvest_date    = logic.get_harvest_date(planting_date, crop_type)

        # 5. Database Persistence
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO farmers_data (
                    farmer_name, crop_type, soil_type, land_area,
                    irrigation_interval, fertilizer_used, fertilizer_cost,
                    date_of_planting, water_usage, yield_tons,
                    sugar_output_kg, harvest_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                farmer_name, crop_type, soil_type, land_area,
                irrigation_interval, fertilizer_used, fertilizer_cost,
                date_of_planting, water_usage, yield_tons,
                sugar_output_kg, harvest_date.strftime("%Y-%m-%d"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()  # Ensure data is written to disk
            record_id = cursor.lastrowid

        return redirect(url_for("result", record_id=record_id))

    except ValueError as ve:
        flash(f"⚠ Input format error: {ve}", "error")
        return redirect(url_for("home"))
    except Exception as e:
        flash(f"⚠ A system error occurred: {e}", "error")
        return redirect(url_for("home"))


@app.route("/result/<int:record_id>")
def result(record_id):
    """Display the detailed analysis for a specific farm record."""
    with get_db() as conn:
        record = conn.execute("SELECT * FROM farmers_data WHERE id = ?", (record_id,)).fetchone()
    
    if record is None:
        flash("⚠ The requested record could not be found.", "error")
        return redirect(url_for("home"))
    
    return render_template("result.html", record=record)


@app.route("/records")
def records():
    """Display a dashboard of all historical farm records."""
    with get_db() as conn:
        all_records = conn.execute("SELECT * FROM farmers_data ORDER BY created_at DESC").fetchall()
    return render_template("records.html", records=all_records)


@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    """Securely delete a record from the database."""
    with get_db() as conn:
        conn.execute("DELETE FROM farmers_data WHERE id = ?", (record_id,))
    flash("✓ Record successfully purged from the system.", "success")
    return redirect(url_for("records"))


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)