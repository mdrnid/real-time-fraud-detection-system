import streamlit as st
import requests
import os
import time
import sqlite3
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield Console",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "data/predictions.db"

# ── Professional Minimalist CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
        background-color: #0f172a !important;
    }
    
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    
    /* Blue Gradient Header */
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #1e3a8a 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-left: 4px solid #3b82f6;
    }
    .header-title { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 0; letter-spacing: -0.02em; }
    .header-sub { font-size: 0.875rem; color: #bfdbfe; opacity: 0.8; margin-top: 0.25rem; }

    /* Minimalist Metrics */
    .metric-box {
        padding: 1.25rem;
        border-bottom: 1px solid #1e293b;
    }
    .metric-label { font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { font-size: 1.75rem; font-weight: 700; color: #f8fafc; margin-top: 0.25rem; }
    
    /* Sidebar Cleanup */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Form & Input Styling */
    .stNumberInput input, .stTextInput input {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 6px !important;
    }
    
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
    }
    .stButton > button:hover { background: #1d4ed8 !important; }

    /* Dataframe custom style */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ── Helper Functions ───────────────────────────────────────────────────────────
def get_live_data(limit=20):
    if not os.path.exists(DB_PATH): return pd.DataFrame()
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT timestamp, transaction_id, amount, prediction, confidence FROM results ORDER BY timestamp DESC LIMIT {limit}", conn)
        conn.close()
        return df
    except: return pd.DataFrame()

def get_stats():
    if not os.path.exists(DB_PATH): return 0, 0, 0
    try:
        conn = sqlite3.connect(DB_PATH)
        total = pd.read_sql_query("SELECT COUNT(*) as c FROM results", conn).iloc[0]['c']
        fraud = pd.read_sql_query("SELECT COUNT(*) as c FROM results WHERE prediction='FRAUD'", conn).iloc[0]['c']
        avg_c = pd.read_sql_query("SELECT AVG(confidence) as a FROM results", conn).iloc[0]['a']
        conn.close()
        return total, fraud, avg_c if avg_c else 0
    except: return 0, 0, 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### System Navigation")
    menu = st.radio("Access Control", ["Overview", "Inference Tool"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### Controls")
    auto_refresh = st.toggle("Auto-Refresh Data", value=True)
    refresh_rate = st.select_slider("Polling Interval", options=[1, 2, 3, 5, 10], value=3)

# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="header-title">Fraud Detection Intelligence</div>
    <div class="header-sub">Enterprise Risk Management System | Live Data Pipeline</div>
</div>
""", unsafe_allow_html=True)

if menu == "Overview":
    total, fraud, avg_conf = get_stats()
    fraud_rate = (fraud / total * 100) if total > 0 else 0

    # Metrics Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Processed</div><div class="metric-value">{total:,}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Fraudulent</div><div class="metric-value" style="color:#ef4444">{fraud:,}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Risk Rate</div><div class="metric-value">{fraud_rate:.2f}%</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Confidence</div><div class="metric-value">{avg_conf:.4f}</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("#### Transaction Monitor")
    df_live = get_live_data(25)
    
    if not df_live.empty:
        st.dataframe(
            df_live,
            use_container_width=True,
            height=450,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="IDR %,.0f"),
                "confidence": st.column_config.NumberColumn("Risk Score", format="%.4f"),
                "timestamp": "Timestamp",
                "transaction_id": "Reference",
                "prediction": st.column_config.TextColumn("Status")
            }
        )
    else:
        st.info("Pipeline active. Awaiting ingestion...")

    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

else:  # Inference Tool
    st.markdown("#### Transaction Verification Tool")
    st.write("Submit features for ad-hoc model inference.")

    with st.container():
        amount = st.number_input("Input Transaction Amount", value=50000.0)
        
        st.write("Feature Vector (V1 - V28)")
        f_cols = st.columns(4)
        v_inputs = []
        for i in range(28):
            with f_cols[i%4]:
                v = st.number_input(f"V{i+1}", value=0.0, format="%.4f", key=f"inf_v{i+1}")
                v_inputs.append(v)
        
        if st.button("Execute Inference"):
            try:
                res = requests.post("http://127.0.0.1:8000/predict_transaction", 
                                   json={"features_v": v_inputs, "amount": amount}, timeout=10)
                result = res.json()
                
                st.markdown("---")
                if result['prediction'] == "FRAUD":
                    st.error(f"Prediction: {result['prediction']} | Score: {result['confidence_score']:.6f}")
                else:
                    st.success(f"Prediction: {result['prediction']} | Score: {result['confidence_score']:.6f}")
            except Exception as e:
                st.error(f"Service Error: {e}")
