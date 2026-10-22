
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Features:
# 1. Requests per minute
# 2. Average interval between requests (seconds)
# 3. Failed attempts per minute

normal_traffic = np.array([
    [1, 60, 0],
    [2, 30, 0],
    [3, 20, 0],
    [2, 25, 1],
    [4, 15, 0],
    [1, 55, 0],
    [3, 18, 1],
    [2, 35, 0],
    [4, 14, 1],
    [3, 22, 0],
    [1, 45, 0],
    [2, 28, 1],
    [3, 25, 0],
    [4, 16, 0],
    [2, 40, 0],
    [1, 50, 1],
    [3, 19, 0],
    [2, 32, 0],
    [4, 13, 1],
    [3, 24, 1],
], dtype=float)

# Normalize features before training
scaler = StandardScaler()
normal_scaled = scaler.fit_transform(normal_traffic)

model = IsolationForest(
    n_estimators=200,
    contamination=0.10,
    random_state=42
)

model.fit(normal_scaled)


def detect_anomaly(
    requests_per_minute,
    avg_interval_seconds,
    failed_attempts_per_minute
):
    features = np.array([[
        requests_per_minute,
        avg_interval_seconds,
        failed_attempts_per_minute
    ]], dtype=float)

    scaled = scaler.transform(features)
    score = float(model.decision_function(scaled)[0])
    prediction = int(model.predict(scaled)[0])

    # Explicit high-risk rule for this demo
    high_risk = (
        requests_per_minute >= 20
        or failed_attempts_per_minute >= 10
        or (
            requests_per_minute >= 10
            and avg_interval_seconds <= 3
        )
    )

    suspicious = high_risk or (
    prediction == -1 and requests_per_minute >= 5
)

    return {
        "prediction": "SUSPICIOUS" if suspicious else "NORMAL",
        "anomaly_score": round(score, 4),
        "high_risk_rule": high_risk
    }


if __name__ == "__main__":
    examples = [
        ("Ordinary traffic", [3, 20, 0]),
        ("Unusual traffic", [100, 0.6, 80]),
    ]

    for name, features in examples:
        print(f"{name}: {detect_anomaly(*features)}")
