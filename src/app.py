from agent.agent import analyze_log
from agent.judge import judge_response
import streamlit as st
import time


st.set_page_config(
    page_title="OpsSentinel AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>

/* 🌌 Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}

/* 🧠 Title */
h1 {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h3 {
    color: #94a3b8;
}

/* 📦 Glass Card */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* 📊 Metric Card */
.metric-card {
    background: linear-gradient(145deg, #1e293b, #020617);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: 0.3s;
}
.metric-card:hover {
    transform: translateY(-5px);
}

/* Labels */
.metric-title {
    color: #94a3b8;
    font-size: 14px;
}

/* Values */
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #3b82f6;
}

/* Severity Colors */
.severity-high { color: #ef4444; font-weight: bold; }
.severity-medium { color: #f59e0b; }
.severity-low { color: #22c55e; }

/* Input */
.stTextArea textarea {
    background: #020617;
    color: #e2e8f0;
    border-radius: 12px;
    border: 1px solid #1e293b;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #22c55e);
    border-radius: 12px;
    height: 3.5em;
    font-weight: bold;
    border: none;
}

/* Fix Cards */
.fix-card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #22c55e;
    transition: 0.3s;
}
.fix-card:hover {
    background: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

st.title("🛡️ DevOps Analayzer")
st.subheader("Next-Gen DevOps Incident Intelligence Platform")

st.markdown("---")

st.markdown("### 📥 Log Input")

user_input = st.text_area(
    label="Add your logs here:",
    height=250,
    placeholder="Paste raw logs here..."
)

run_btn = st.button("Run Intelligent Diagnostics", use_container_width=True)

st.markdown("---")

if run_btn:

    if not user_input.strip():
        st.error("⚠️ Please enter logs before running analysis")
    else:
        with st.spinner("🧠 AI analyzing system behavior..."):
            time.sleep(1)

            response = analyze_log(user_input)
            data = response.model_dump()

            judge = judge_response(user_input, data)

        st.success("✅ Analysis Completed Successfully")

        # ===============================
        # 📊 Metrics Dashboard
        # ===============================
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Issue Type</div>
            <div class="metric-value">{data["issue_type"]}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Confidence</div>
            <div class="metric-value">{data["confidence"]}%</div>
        </div>
        """, unsafe_allow_html=True)

        # Severity Logic
        if data["confidence"] > 85:
            severity = "CRITICAL"
            severity_class = "severity-high"
        elif data["confidence"] > 60:
            severity = "WARNING"
            severity_class = "severity-medium"
        else:
            severity = "LOW"
            severity_class = "severity-low"

        col3.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Severity</div>
            <div class="{severity_class}">{severity}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div class="card">
            <h4>🔍 Root Cause Analysis</h4>
            <p>{data["root_cause"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🛠️ Recommended Fixes")

        for i, step in enumerate(data["suggested_fixes"], 1):
            st.markdown(f"""
            <div class="fix-card">
                <b>Step {i}:</b> {step}
            </div>
            """, unsafe_allow_html=True)


        st.markdown("### ⚖️ AI Evaluation")

        col_j1, col_j2 = st.columns([1, 3])

        col_j1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Score</div>
            <div class="metric-value">{judge["score"]}/10</div>
        </div>
        """, unsafe_allow_html=True)

        col_j2.markdown(f"""
        <div class="card">
            <h4>💬 Feedback</h4>
            <p>{judge["feedback"]}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("💡 Paste logs and run diagnostics to see AI insights")
