# =====================================
# Flask App - Portfolio Project (Fullstack)
# =====================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os, sys, requests

# ----------------------------
# Fix Import Paths (Render & Local)
# ----------------------------
if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(__file__))
    from routes.projects import projects_bp
else:
    from server.routes.projects import projects_bp

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Initialize Flask app
# ----------------------------
app = Flask(__name__, static_folder=None)

# ----------------------------
# Register Blueprints FIRST
# ----------------------------
app.register_blueprint(projects_bp)

# ----------------------------
# CORS Setup
# ----------------------------
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "https://portfolio-project-x2xz.onrender.com",
        "https://sachinportfolio.com",
        "https://www.sachinportfolio.com"
    ],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
)

# ----------------------------
# Contact Form (SendGrid)
# ----------------------------
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not (name and email and message):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    CONTACT_RECEIVER = os.getenv("CONTACT_RECEIVER")

    if not SENDGRID_API_KEY or not CONTACT_RECEIVER:
        print("❌ Missing SENDGRID_API_KEY or CONTACT_RECEIVER environment variable.")
        return jsonify({"status": "error", "message": "Server misconfiguration."}), 500

    payload = {
        "personalizations": [{
            "to": [{"email": CONTACT_RECEIVER}],
            "subject": f"New Contact Form Message from {name}"
        }],
        "from": {"email": "cuffsachin@gmail.com"},
        "content": [{
            "type": "text/plain",
            "value": f"From: {name} <{email}>\n\nMessage:\n{message}"
        }]
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )
        if response.status_code == 202:
            print("✅ Email sent successfully via SendGrid!")
            return jsonify({"status": "success", "message": "Email sent successfully!"}), 200
        else:
            print(f"❌ SendGrid responded with {response.status_code}: {response.text}")
            return jsonify({"status": "error", "message": "SendGrid failed.", "details": response.text}), 500
    except Exception as e:
        print("❌ SendGrid error:", e)
        return jsonify({"status": "error", "message": "Failed to send email."}), 500


# ----------------------------
# Serve React Frontend (SPA)
# ----------------------------
@app.route("/static/<path:path>")
def serve_static(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))
    return send_from_directory(os.path.join(build_dir, "static"), path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))
    file_path = os.path.join(build_dir, path)
    if path and os.path.exists(file_path):
        return send_from_directory(build_dir, path)
    return send_from_directory(build_dir, "index.html")


# ----------------------------
# Run the App (Local only)
# ----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
