import os, sys

# Allow both local (`python app.py`) and Render (`gunicorn server.app:app`) runs
if __package__ is None or __package__ == "":
    # running locally → we're already inside `server/`
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from db_connect import get_db_connection
else:
    # running as package on Render
    from server.db_connect import get_db_connection

from flask import Blueprint, jsonify


# Prefix ensures API endpoints live under /api/
projects_bp = Blueprint("projects_bp", __name__, url_prefix="/api")

@projects_bp.route("/projects", methods=["GET"])
def get_projects():
    conn = None
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute query
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        columns = [col[0] for col in cursor.description]
        projects = [dict(zip(columns, row)) for row in rows]

        # Close resources
        cursor.close()
        conn.close()

        # Return JSON response
        return jsonify({"projects": projects}), 200

    except Exception as e:
        # Safely close connection if something goes wrong
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500
