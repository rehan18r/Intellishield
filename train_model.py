import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Synthetic dataset generation for API request traffic
# Features: request_rate (req/min), avg_interval (sec), ua_entropy (0-1), time_of_day (0-23)
np.random.seed(42)

normal_traffic = np.random.multivariate_normal(
    mean=[3.5, 25.0, 0.15, 13.5],
    cov=[[2.0, -8.0, 0.0, 0.5],
         [-8.0, 120.0, 0.0, -2.0],
         [0.0, 0.0, 0.02, 0.0],
         [0.5, -2.0, 0.0, 16.0]],
    size=400
)

attack_traffic = np.random.multivariate_normal(
    mean=[45.0, 1.2, 0.92, 2.0],
    cov=[[15.0, -15.0, 0.1, 3.0],
         [-15.0, 35.0, -0.05, -1.0],
         [0.1, -0.05, 0.03, 0.0],
         [3.0, -1.0, 0.0, 22.0]],
    size=100
)

# Clip and sanitize
normal_traffic[:, 0] = np.clip(normal_traffic[:, 0], 0.5, 15)
normal_traffic[:, 1] = np.clip(normal_traffic[:, 1], 3, 120)
normal_traffic[:, 2] = np.clip(normal_traffic[:, 2], 0, 1)
normal_traffic[:, 3] = np.clip(normal_traffic[:, 3], 0, 23)

attack_traffic[:, 0] = np.clip(attack_traffic[:, 0], 15, 120)
attack_traffic[:, 1] = np.clip(attack_traffic[:, 1], 0.1, 5)
attack_traffic[:, 2] = np.clip(attack_traffic[:, 2], 0.6, 1)
attack_traffic[:, 3] = np.clip(attack_traffic[:, 3], 0, 23)

X = np.vstack([normal_traffic, attack_traffic])
y = np.hstack([np.zeros(len(normal_traffic)), np.ones(len(attack_traffic))])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    n_estimators=300,
    contamination=0.22,
    random_state=42,
    max_samples='auto',
    bootstrap=False
)
model.fit(X_scaled)

joblib.dump({"model": model, "scaler": scaler}, "intellishield_model.pkl")
print("Trained and saved to intellishield_model.pkl")
