from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import send_from_directory
from routes.projects import projects_bp

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Serve React build files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/build"))
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, "index.html")


# --- CORS setup ---
CORS(
    app,
    origins=["http://localhost:3000", "https://portfolio-project-pdp5.onrender.com/"],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
)

# --- Mail config ---
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
)

mail = Mail(app)

# --- Preflight handler (safeguard) ---
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        headers = response.headers
        headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response


# --- Contact endpoint ---
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
        print("Email sent successfully!")
        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"status": "error", "message": "Failed to send email."}), 500


# --- Register blueprint & run ---
app.register_blueprint(projects_bp)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
