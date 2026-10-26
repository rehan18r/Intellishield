
from collections import defaultdict, deque
from time import monotonic

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ml_model import detect_anomaly
from database import init_db, log_request

app = FastAPI(
    title="IntelliShield API Firewall",
    version="1.0.0",
    description="ML-driven protection against simulated call and SMS bombing"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://intellishield.vercel.app",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

WINDOW_SECONDS = 60
MAX_REQUESTS = 5

request_history = defaultdict(deque)

# Create the database table if it does not exist.
init_db()


class VerificationRequest(BaseModel):
    account_id: str = Field(min_length=1, max_length=40)
    channel: str


@app.get("/")
def home():
    return {
        "project": "IntelliShield",
        "status": "running",
        "protection": "Rate limiting + ML anomaly detection"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/request-verification")
def request_verification(data: VerificationRequest):
    if data.channel not in ("sms", "call"):
        raise HTTPException(
            status_code=400,
            detail="Channel must be sms or call"
        )

    now = monotonic()
    history = request_history[data.account_id]

    while history and now - history[0] >= WINDOW_SECONDS:
        history.popleft()

    history.append(now)

    request_count = len(history)
    requests_per_minute = request_count * 60 / WINDOW_SECONDS

    if request_count > 1:
        intervals = [
            history[i] - history[i - 1]
            for i in range(1, len(history))
        ]
        avg_interval = sum(intervals) / len(intervals)
    else:
        avg_interval = 60.0

    # Failed attempts are not measured in this simulation.
    failed_attempts_per_minute = 0

    ml_result = detect_anomaly(
        requests_per_minute,
        avg_interval,
        failed_attempts_per_minute
    )

    # Temporary warm-up rule to reduce early false positives.
    if request_count < 3:
        ml_result["prediction"] = "NORMAL"
        ml_result["high_risk_rule"] = False

    # Enforce the hard request limit and log BLOCK decisions.
    if request_count > MAX_REQUESTS:
        log_request(
            data.account_id,
            data.channel,
            request_count,
            ml_result["prediction"],
            ml_result["anomaly_score"],
            "BLOCK"
        )

        raise HTTPException(
            status_code=429,
            detail={
                "account_id": data.account_id,
                "channel": data.channel,
                "decision": "BLOCK",
                "reason": "Request rate limit exceeded",
                "requests_in_window": request_count,
                "ml_detection": ml_result
            }
        )

    # Log suspicious requests.
    if ml_result["prediction"] == "SUSPICIOUS":
        log_request(
            data.account_id,
            data.channel,
            request_count,
            ml_result["prediction"],
            ml_result["anomaly_score"],
            "FLAG"
        )

        return {
            "account_id": data.account_id,
            "channel": data.channel,
            "decision": "FLAG",
            "requests_in_window": request_count,
            "ml_detection": ml_result,
            "message": "Suspicious behavior detected; no message was sent."
        }

    # Log normal requests.
    log_request(
        data.account_id,
        data.channel,
        request_count,
        ml_result["prediction"],
        ml_result["anomaly_score"],
        "ALLOW"
    )

    return {
        "account_id": data.account_id,
        "channel": data.channel,
        "decision": "ALLOW",
        "requests_in_window": request_count,
        "ml_detection": ml_result,
        "message": "Simulation only; no message was sent."
    }
