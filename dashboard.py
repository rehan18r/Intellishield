
import streamlit as st
import pandas as pd
from database import get_logs

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IntelliShield | Security Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080d18;
    color: #e8eefc;
}

[data-testid="stSidebar"] {
    background: #0d1424;
    border-right: 1px solid #202b40;
}

[data-testid="stSidebar"] * {
    color: #e8eefc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.hero {
    background: linear-gradient(120deg, #111d35, #10162a);
    border: 1px solid #263958;
    border-radius: 18px;
    padding: 25px 28px;
    margin-bottom: 24px;
}

.hero h1 {
    margin: 0;
    font-size: 31px;
    font-weight: 800;
    color: #f1f5ff;
}

.hero p {
    color: #9baecc;
    margin-bottom: 0;
    margin-top: 8px;
}

.eyebrow {
    color: #64e6c2;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 9px;
}

.metric-card {
    background: linear-gradient(145deg, #121d31, #0e1728);
    border: 1px solid #25344c;
    border-radius: 15px;
    padding: 20px;
    min-height: 132px;
}

.metric-label {
    color: #9baecc;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #f2f6ff;
    margin-top: 10px;
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 10px;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #f1f5ff;
    margin: 20px 0 12px 0;
}

.status-pill {
    display: inline-block;
    background: #12372f;
    color: #65e6bd;
    border: 1px solid #246b58;
    padding: 6px 12px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #26344b;
    border-radius: 12px;
    overflow: hidden;
}

.stButton button {
    border-radius: 9px;
    border: 1px solid #2d4569;
    background: #172944;
    color: white;
    font-weight: 600;
}

.stButton button:hover {
    border-color: #5e9dff;
    color: white;
}

hr {
    border-color: #26344b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
try:
    logs = get_logs()
    df = pd.DataFrame(logs) if logs else pd.DataFrame()
except Exception as e:
    st.error(f"Could not load database logs: {e}")
    st.stop()

if not df.empty:
    for col in [
        "account_id", "channel", "requests_in_window",
        "prediction", "anomaly_score", "decision", "timestamp"
    ]:
        if col not in df.columns:
            df[col] = None

    df["decision"] = df["decision"].fillna("UNKNOWN").astype(str).str.upper()
    df["channel"] = df["channel"].fillna("unknown").astype(str).str.upper()
    df["prediction"] = df["prediction"].fillna("UNKNOWN").astype(str).str.upper()
    df["timestamp"] = df["timestamp"].astype(str)

    df = df.sort_values("id", ascending=False) if "id" in df.columns else df

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🛡️ IntelliShield")
    st.caption("AI SECURITY MONITOR")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Request Logs", "Model Insights"],
        label_visibility="visible"
    )

    st.divider()
    st.markdown("### System status")
    st.markdown(
        '<span class="status-pill">● LOCAL PROTOTYPE</span>',
        unsafe_allow_html=True
    )
    st.caption("API: http://127.0.0.1:8000")
    st.caption("Database: SQLite")
    st.caption("Detection: Isolation Forest")

    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.rerun()

    st.divider()
    st.caption("IntelliShield • Academic Project")

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">SECURITY OPERATIONS CENTER</div>
    <h1>IntelliShield Dashboard</h1>
    <p>ML-driven monitoring of simulated call and SMS verification requests.</p>
</div>
""", unsafe_allow_html=True)

total = len(df)
allowed = int((df["decision"] == "ALLOW").sum()) if total else 0
flagged = int((df["decision"] == "FLAG").sum()) if total else 0
blocked = int((df["decision"] == "BLOCK").sum()) if total else 0
suspicious = int((df["prediction"] == "SUSPICIOUS").sum()) if total else 0

# ---------------- OVERVIEW ----------------
if page == "Overview":

    st.markdown("### Live activity summary")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "📡", "TOTAL REQUESTS", total),
        (c2, "✅", "ALLOWED", allowed),
        (c3, "⚠️", "FLAGGED", flagged),
        (c4, "🚫", "BLOCKED", blocked),
    ]

    for col, icon, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Traffic analytics</div>',
                unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Security decisions")
        if total:
            decisions = df["decision"].value_counts()
            st.bar_chart(decisions, color="#48d9b0")
        else:
            st.info("No request data yet. Send a test request to the API.")

    with right:
        st.markdown("#### Request channels")
        if total:
            channels = df["channel"].value_counts()
            st.bar_chart(channels, color="#6c9cff")
        else:
            st.info("Channel analytics will appear here.")

    st.markdown('<div class="section-title">Recent activity</div>',
                unsafe_allow_html=True)

    if total:
        show_cols = [
            c for c in [
                "timestamp", "account_id", "channel",
                "requests_in_window", "prediction", "decision"
            ] if c in df.columns
        ]
        st.dataframe(
            df[show_cols].head(8),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Your request history will appear here.")

# ---------------- REQUEST LOGS ----------------
elif page == "Request Logs":

    st.markdown("### Request history")
    st.caption("Review the simulated requests recorded in SQLite.")

    if total:
        f1, f2 = st.columns(2)

        with f1:
            decision_options = ["All"] + sorted(df["decision"].unique().tolist())
            selected_decision = st.selectbox(
                "Filter by decision", decision_options
            )

        with f2:
            channel_options = ["All"] + sorted(df["channel"].unique().tolist())
            selected_channel = st.selectbox(
                "Filter by channel", channel_options
            )

        filtered = df.copy()

        if selected_decision != "All":
            filtered = filtered[filtered["decision"] == selected_decision]

        if selected_channel != "All":
            filtered = filtered[filtered["channel"] == selected_channel]

        st.write(f"**{len(filtered)}** matching records")

        display_cols = [
            c for c in [
                "id", "timestamp", "account_id", "channel",
                "requests_in_window", "prediction", "anomaly_score", "decision"
            ] if c in filtered.columns
        ]

        st.dataframe(
            filtered[display_cols],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download CSV",
            data=filtered[display_cols].to_csv(index=False).encode("utf-8"),
            file_name="intellishield_logs.csv",
            mime="text/csv"
        )
    else:
        st.info("No logs found. Test the API first.")

# ---------------- MODEL INSIGHTS ----------------
elif page == "Model Insights":

    st.markdown("### Machine learning insights")
    st.caption("Isolation Forest anomaly detection results.")

    m1, m2 = st.columns(2)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SUSPICIOUS PREDICTIONS</div>
            <div class="metric-value">{suspicious}</div>
            <p style="color:#9baecc;">Requests labelled suspicious by the recorded model output.</p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        normal = int((df["prediction"] == "NORMAL").sum()) if total else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">NORMAL PREDICTIONS</div>
            <div class="metric-value">{normal}</div>
            <p style="color:#9baecc;">Requests labelled normal by the recorded model output.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Prediction distribution")
    if total:
        st.bar_chart(df["prediction"].value_counts(), color="#a78bfa")
    else:
        st.info("Model insights will appear after requests are logged.")

    st.warning(
        "This is an academic prototype using synthetic training data. "
        "These counts are not a measure of model accuracy or production security."
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "IntelliShield | Educational prototype | Simulated traffic only"
)
