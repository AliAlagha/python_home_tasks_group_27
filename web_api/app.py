import os

import pymysql
from flask import Flask, jsonify, render_template, request

from web_api.errors import ApiError

app = Flask(__name__)

# login data for MySQL, can be changed with environment variables
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "waste_sorting"),
}


def run_query(sql, values=()):
    try:
        connection = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    except pymysql.MySQLError:
        raise ApiError("database is not available", 503)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            scans = cursor.fetchall()
    except pymysql.MySQLError:
        raise ApiError("database query failed", 500)
    finally:
        connection.close()
    # dates can not go into json directly
    for scan in scans:
        if "scan_date" in scan:
            scan["scan_date"] = str(scan["scan_date"])
    return scans


# errors are sent back as json instead of the default html page
@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify({"error": str(error)}), error.status_code


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "page not found"}), 404


@app.route("/")
def index():
    scans = run_query("SELECT * FROM scan_records ORDER BY scan_date DESC")
    return render_template("index.html", scans=scans)


@app.route("/api/scans")
def api_scans():
    region = request.args.get("region")
    if region:
        sql = "SELECT * FROM scan_records WHERE region_name = %s ORDER BY scan_date DESC"
        return jsonify(run_query(sql, (region,)))
    return jsonify(run_query("SELECT * FROM scan_records ORDER BY scan_date DESC"))


@app.route("/api/scans/<int:scan_id>")
def api_scan(scan_id):
    scans = run_query("SELECT * FROM scan_records WHERE scan_id = %s", (scan_id,))
    if len(scans) == 0:
        raise ApiError("scan not found", 404)
    return jsonify(scans[0])


# MySQL does the counting with GROUP BY
@app.route("/api/statistics")
def api_statistics():
    total = run_query("SELECT COUNT(*) AS amount FROM scan_records")[0]["amount"]
    categories = run_query("SELECT category, COUNT(*) AS amount FROM scan_records GROUP BY category")
    items = run_query("SELECT item_name, COUNT(*) AS amount FROM scan_records "
                      "GROUP BY item_name ORDER BY amount DESC LIMIT 5")

    composition = {}
    for row in categories:
        composition[row["category"]] = row["amount"]

    rate = 0
    if total > 0:
        rate = round(composition.get("Recyclable", 0) / total * 100, 1)

    most_common = {}
    for row in items:
        most_common[row["item_name"]] = row["amount"]

    return jsonify({
        "scans": total,
        "waste_composition": composition,
        "recycling_rate": rate,
        "most_common_items": most_common,
    })


if __name__ == "__main__":
    app.run(port=5001)
