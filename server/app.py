# =====================================
# Flask App - Portfolio Project (Fullstack on Render)
# =====================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os, sys
import requests
import traceback

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
    ],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
)

# ----------------------------
# Flask-Mail Configuration
# ----------------------------
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
)
mail = Mail(app)

# ----------------------------
# Contact Form Endpoint
# ----------------------------
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not (name and email and message):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Prepare SendGrid payload
    payload = {
        "personalizations": [{
            "to": [{"email": os.getenv("CONTACT_RECEIVER")}],
            "subject": f"New Contact Form Message from {name}"
        }],
        "from": {"email": "no-reply@sachinportfolio.com"},
        "content": [{
            "type": "text/plain",
            "value": f"From: {name} <{email}>\n\nMessage:\n{message}"
        }]
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {os.getenv('SENDGRID_API_KEY')}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        print("✅ Email sent successfully via SendGrid!")
        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200
    except Exception as e:
        print("❌ SendGrid error:", e)
        return jsonify({"status": "error", "message": "Failed to send email."}), 500


# ----------------------------
# Serve React Frontend (SPA)
# ----------------------------

# Serve static files like JS and CSS
@app.route("/static/<path:path>")
def serve_static(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))
    return send_from_directory(os.path.join(build_dir, "static"), path)

# Serve index.html and React routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))

    # Serve file if it exists
    file_path = os.path.join(build_dir, path)
    if path and os.path.exists(file_path):
        return send_from_directory(build_dir, path)

    # Fallback to index.html
    return send_from_directory(build_dir, "index.html")

# ----------------------------
# Run the App (Local only)
# ----------------------------
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5000))
    except ValueError:
        port = 5000
    app.run(debug=True, host="0.0.0.0", port=port)
