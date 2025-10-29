# =====================================
# Flask App - Portfolio Project (Render Optimized)
# =====================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os, sys
# Allow both local and Render runs
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
# Serve Static Files (JS, CSS, Media)
# ----------------------------
@app.route("/static/<path:filename>")
def serve_static(filename):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "build"))
    static_dir = os.path.join(build_dir, "static")
    full_path = os.path.join(static_dir, filename)
    print("🔍 Serving static file:", full_path, "exists?", os.path.exists(full_path))
    return send_from_directory(static_dir, filename)


# ----------------------------
# Serve React Frontend
# ----------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "build"))

    # Serve files that exist directly in build/ (favicon, manifest, etc.)
    file_path = os.path.join(build_dir, path)
    if path and os.path.exists(file_path):
        return send_from_directory(build_dir, path)

    # React Router fallback
    return send_from_directory(build_dir, "index.html")


# -------------------------------------
# 🔍 Debug route for Render visibility
# -------------------------------------
@app.route("/debug/build")
def debug_build():
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "build"))
    static_dir = os.path.join(build_dir, "static")
    exists_main_js = os.path.exists(os.path.join(static_dir, "js/main.3dd403c7.js"))
    exists_main_css = os.path.exists(os.path.join(static_dir, "css/main.4a5877b2.css"))

    files = []
    if os.path.exists(build_dir):
        for root, dirs, filenames in os.walk(build_dir):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), build_dir)
                files.append(rel_path)

    return {
        "build_dir": build_dir,
        "static_dir": static_dir,
        "exists_main_js": exists_main_js,
        "exists_main_css": exists_main_css,
        "total_files_found": len(files),
        "example_files": files[:10]
    }

# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5001))
    except ValueError:
        port = 5001

    app.run(debug=True, host="0.0.0.0", port=port)
