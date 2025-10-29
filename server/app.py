# =====================================
# Flask App - Portfolio Project
# =====================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from routes.projects import projects_bp
import os
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Initialize Flask app
# ----------------------------
app = Flask(__name__)

# ----------------------------
# Register Blueprints FIRST
# (So /api/* routes are handled before static files)
# ----------------------------
app.register_blueprint(projects_bp)

# ----------------------------
# CORS Setup
# ----------------------------
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://portfolio-project-pdp5.onrender.com"
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

    msg = Message(
        subject=f"New Contact Form Message from {name}",
        recipients=[os.getenv("CONTACT_RECEIVER")],
        body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
    )

    try:
        mail.send(msg)
        print("✅ Email sent successfully!")
        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200
    except Exception as e:
        print("❌ Error sending email:", e)
        return jsonify({"status": "error", "message": "Failed to send email."}), 500


# ----------------------------
# Serve React Frontend (after API routes)
# ----------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))

    # Serve static assets (JS, CSS, images)
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)

    # Otherwise, serve index.html for React Router
    return send_from_directory(build_dir, "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))
    return send_from_directory(os.path.join(build_dir, "static"), filename)


# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5001))  # ✅ safely defaults to 5001
    except ValueError:
        port = 5001
    app.run(debug=True, host="0.0.0.0", port=port)

