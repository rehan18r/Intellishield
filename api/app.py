from flask import Flask, request, jsonify, abort, render_template_string
import joblib
import sqlite3
import numpy as np
from database import init_db, log_decision, get_stats

app = Flask(__name__)
init_db()

ml_bundle = joblib.load("intellishield_model.pkl")
model = ml_bundle["model"]
scaler = ml_bundle["scaler"]

@app.before_request
def intellishield_firewall():
    if request.path == "/api/send-otp" and request.method == "POST":
        ip = request.remote_addr or "127.0.0.1"
        ua_header = request.headers.get("User-Agent", "")
        ua_randomness = min(1.0, len(set(ua_header.split())) / 10.0) if ua_header else 0.0
        conn = sqlite3.connect("/tmp/intellishield.db")
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
        ml_prediction = "Blocked" if prediction_raw == -1 else "Allowed"
        if request_rate > 25:
            ml_prediction = "Blocked"
        log_decision(ip, "/api/send-otp", round(float(request_rate), 2), round(float(ua_entropy), 2), ml_prediction)
        if ml_prediction == "Blocked":
            return abort(403, description={"status":"Blocked","message":"IntelliShield firewall blocked this request."})

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    return jsonify({"status":"Allowed","message":"Simulation only; no real SMS or call was sent."})

@app.route("/api/stats")
def stats():
    return jsonify(get_stats())

# Default handler for Vercel serverless
handler = app
