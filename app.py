import joblib
import sqlite3
import numpy as np
from flask import Flask, request, jsonify, render_template, abort
from database import init_db, log_decision, get_stats

app = Flask(__name__, template_folder="templates", static_folder="static")

init_db()

ml_bundle = joblib.load("intellishield_model.pkl")
model = ml_bundle["model"]
scaler = ml_bundle["scaler"]


@app.before_request
def intellishield_firewall():
    # Only intercept the mock OTP endpoint
    if request.path == "/api/send-otp" and request.method == "POST":
        # Simulate feature extraction from incoming request
        ip = request.remote_addr or "127.0.0.1"
        # Entropy and randomness simulation based on header presence
        ua_header = request.headers.get("User-Agent", "")
        ua_randomness = min(1.0, len(set(ua_header.split())) / 10.0) if ua_header else 0.0

        # Simulated request rate based on a simple session counter
        conn = sqlite3.connect("intellishield.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE ip_address = ?", (ip,))
        recent_count = cursor.fetchone()[0]
        conn.close()

        request_rate = min(recent_count + 2, 50) + np.random.uniform(-1, 5)
        avg_interval = max(60.0 / (request_rate + 1), 0.5)
        ua_entropy = min(ua_randomness + np.random.uniform(0, 0.3), 1.0)
        time_of_day = np.random.uniform(0, 23)

        features = np.array([[request_rate, avg_interval, ua_entropy, time_of_day]])
        scaled = scaler.transform(features)
        score = float(model.decision_function(scaled)[0])
        prediction_raw = int(model.predict(scaled)[0])

        # Map Isolation Forest output: -1 = anomaly (Blocked), 1 = normal (Allowed)
        ml_prediction = "Blocked" if prediction_raw == -1 else "Allowed"

        # Force high-rate patterns to blocked for demo coherence
        if request_rate > 25:
            ml_prediction = "Blocked"

        log_decision(
            ip_address=ip,
            endpoint="/api/send-otp",
            request_rate=round(float(request_rate), 2),
            user_agent_score=round(float(ua_entropy), 2),
            ml_prediction=ml_prediction
        )

        if ml_prediction == "Blocked":
            return abort(403, description={
                "status": "Blocked",
                "message": "IntelliShield firewall blocked this request. Anomalous traffic pattern detected."
            })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    # If firewall allowed it, return success
    return jsonify({
        "status": "Allowed",
        "message": "Simulation only; no real SMS or call was sent."
    })


@app.route("/api/stats")
def stats():
    return jsonify(get_stats())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
