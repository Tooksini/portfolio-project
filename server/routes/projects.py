from flask import Blueprint, jsonify
from db_connect import get_db_connection

projects_bp = Blueprint("projects_bp", __name__)

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

        # Convert rows to list of dictionaries for JSON output
        columns = [col[0] for col in cursor.description]
        projects = [dict(zip(columns, row)) for row in rows]

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return JSON response
        return jsonify({"success": True, "projects": projects}), 200

    except Exception as e:
        # Handle errors
        if conn:
            conn.close()
        return jsonify({"success": False, "error": str(e)}), 500
