from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="JaiShreeRam@214#",
        database="cyber_incident_db"
    )


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Report Incident
@app.route("/report", methods=["GET", "POST"])
def report():

    if request.method == "POST":

        title = request.form["title"]
        incident_type = request.form["incident_type"]
        description = request.form["description"]
        severity = request.form["severity"]
        location = request.form["location"]
        incident_date = request.form["incident_date"]

        db = get_db_connection()
        cursor = db.cursor()

        sql = """
        INSERT INTO incidents
        (user_id, title, incident_type, description,
        severity, location, incident_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            1,
            title,
            incident_type,
            description,
            severity,
            location,
            incident_date,
            "Reported"
        )

        cursor.execute(sql, values)

        db.commit()

        cursor.close()
        db.close()

        return "Incident reported successfully!"

    return render_template("report.html")


# View Incidents
@app.route("/incidents")
def incidents():

    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    SELECT incident_id, title, incident_type,
           severity, location, incident_date, status
    FROM incidents
    """

    cursor.execute(sql)

    incidents = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "incidents.html",
        incidents=incidents
    )


# Admin Page
@app.route("/admin")
def admin():

    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    SELECT incident_id, title, incident_type,
           severity, status
    FROM incidents
    """

    cursor.execute(sql)

    incidents = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin.html",
        incidents=incidents
    )


# Update Status
@app.route("/update_status", methods=["POST"])
def update_status():

    incident_id = request.form["incident_id"]
    status = request.form["status"]

    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    UPDATE incidents
    SET status = %s
    WHERE incident_id = %s
    """

    cursor.execute(sql, (status, incident_id))

    db.commit()

    cursor.close()
    db.close()

    return "Status updated successfully!"


if __name__ == "__main__":
    app.run(debug=True)