import streamlit as st
import requests
import os
import random
import time

st.set_page_config(
    page_title="FraudShield — Real-time Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"], button { font-family: 'DM Sans', sans-serif !important; }

    .stApp { background: #09111f; color: #d1d9e6; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 3rem; max-width: 1400px; }

    .hero {
        padding: 2.25rem 2.75rem;
        background: linear-gradient(135deg, #0c1829 0%, #111d38 60%, #0c1829 100%);
        border: 1px solid rgba(88, 101, 242, 0.18);
        border-radius: 14px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 360px; height: 360px;
        background: radial-gradient(circle, rgba(88, 101, 242, 0.07) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10b981;
        font-size: 0.68rem;
        font-weight: 600;
        padding: 3px 11px;
        border-radius: 20px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .hero-eyebrow .indicator {
        width: 5px; height: 5px;
        background: #10b981;
        border-radius: 50%;
        animation: blink 2s ease-in-out infinite;
        display: inline-block;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.2; }
    }
    .hero-title {
        font-size: 1.95rem; font-weight: 700; color: #eef1f7;
        margin: 0; line-height: 1.2; letter-spacing: -0.02em;
    }
    .hero-title .accent {
        background: linear-gradient(135deg, #7c84f7, #b87af8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub { font-size: 0.875rem; color: #4f6279; margin-top: 0.55rem; line-height: 1.6; }

    .stat-card {
        background: #0e1b2e;
        border: 1px solid #1a2d47;
        border-radius: 10px;
        padding: 1.1rem 1rem;
        text-align: center;
    }
    .stat-val {
        font-size: 1.45rem; font-weight: 700; color: #7c84f7;
        display: block; line-height: 1; letter-spacing: -0.02em;
        font-family: 'DM Mono', monospace !important;
    }
    .stat-lbl {
        font-size: 0.68rem; color: #3d5068; text-transform: uppercase;
        letter-spacing: 0.08em; margin-top: 0.45rem; display: block; font-weight: 600;
    }

    .panel {
        background: rgba(14, 27, 46, 0.4);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border: none;
    }
    .panel-title {
        font-size: 0.8rem; font-weight: 700; letter-spacing: 0.1em;
        text-transform: uppercase; color: #7c84f7;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .panel-title::before {
        content: '';
        width: 4px; height: 16px;
        background: linear-gradient(to bottom, #5865f2, #7a5af8);
        border-radius: 4px;
    }

    /* Amount display */
    .amount-display {
        font-family: 'DM Mono', monospace;
        font-size: 1.5rem;
        font-weight: 500;
        color: #7c84f7;
        letter-spacing: -0.02em;
        padding: 0.5rem 0 0.75rem;
    }
    .amount-display .currency-label {
        font-size: 0.78rem;
        color: #3d5068;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-right: 6px;
        vertical-align: middle;
    }

    .stNumberInput > label {
        font-size: 0.75rem !important; font-weight: 500 !important;
        color: #5f7a98 !important; letter-spacing: 0.01em !important;
    }
    .stNumberInput input, .stTextInput input {
        background: #081420 !important;
        border: 1px solid #1a2d47 !important;
        border-radius: 8px !important;
        color: #d1d9e6 !important;
        font-size: 0.85rem !important;
        font-family: 'DM Mono', monospace !important;
        padding: 0.6rem 0.8rem !important;
    }
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #5865f2 !important;
        box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.1) !important;
    }
    /* Hide the box around the entire input widget and columns */
    div[data-testid="stVerticalBlockBorderWrapper"], 
    div[data-testid="column"],
    div[data-testid="stVerticalBlock"] > div {
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stNumberInput"] {
        margin-bottom: -0.5rem !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #5865f2, #7a5af8) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.01em !important;
        width: 100%;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
        box-shadow: 0 3px 16px rgba(88, 101, 242, 0.28) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(88, 101, 242, 0.42) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    .btn-ghost .stButton > button {
        background: #0e1b2e !important;
        color: #5f7a98 !important;
        border: 1px solid #1a2d47 !important;
        box-shadow: none !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
    }
    .btn-ghost .stButton > button:hover {
        background: #132235 !important;
        color: #c5d0de !important;
        border-color: #5865f2 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .result-fraud {
        background: linear-gradient(135deg, rgba(220,38,38,0.07), rgba(185,28,28,0.03));
        border: 1px solid rgba(220,38,38,0.25);
        border-radius: 12px; padding: 2rem 1.5rem; text-align: center;
    }
    .result-safe {
        background: linear-gradient(135deg, rgba(5,150,105,0.07), rgba(4,120,87,0.03));
        border: 1px solid rgba(5,150,105,0.25);
        border-radius: 12px; padding: 2rem 1.5rem; text-align: center;
    }
    .result-heading-fraud { font-size: 1.6rem; font-weight: 700; color: #f87171; letter-spacing: -0.02em; margin-top: 0.5rem; }
    .result-heading-safe  { font-size: 1.6rem; font-weight: 700; color: #34d399; letter-spacing: -0.02em; margin-top: 0.5rem; }
    .result-sub { color: #4f6279; font-size: 0.83rem; margin-top: 0.3rem; }

    .bar-track { background: #132235; border-radius: 99px; height: 6px; margin: 1.25rem 0; overflow: hidden; }
    .bar-fraud { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #b91c1c, #ef4444); }
    .bar-safe  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #047857, #10b981); }

    .score-number {
        font-size: 2.1rem; font-weight: 700;
        font-family: 'DM Mono', monospace !important;
        letter-spacing: -0.03em;
    }
    .score-number.fraud { color: #f87171; }
    .score-number.safe  { color: #34d399; }
    .score-label { font-size: 0.72rem; color: #4f6279; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 2px; }

    .pill {
        display: inline-flex; align-items: center; gap: 5px;
        background: #0e1b2e; border: 1px solid #1a2d47;
        border-radius: 7px; padding: 5px 11px;
        font-size: 0.73rem; color: #5f7a98; margin: 3px;
        font-family: 'DM Mono', monospace !important;
    }
    .pill .pill-lbl {
        font-size: 0.68rem; color: #3d5068; text-transform: uppercase;
        letter-spacing: 0.06em; margin-right: 2px;
        font-family: 'DM Sans', sans-serif !important;
    }
    .pill strong { color: #c5d0de; }

    .awaiting-state { text-align: center; padding: 5rem 1rem; }
    .awaiting-icon {
        width: 44px; height: 44px; border: 2px solid #1a2d47;
        border-radius: 10px; display: flex; align-items: center;
        justify-content: center; margin: 0 auto 1.25rem; background: #132235;
    }
    .awaiting-title { font-size: 0.9rem; color: #3d5068; font-weight: 600; }
    .awaiting-sub   { font-size: 0.78rem; color: #263d55; margin-top: 0.35rem; }

    div[data-testid="stExpander"] {
        background: transparent !important;
        border: 1px solid rgba(26, 45, 71, 0.5) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] > details {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────────────
if "pending_reset" not in st.session_state:
    st.session_state.pending_reset = False
if "pending_randomize" not in st.session_state:
    st.session_state.pending_randomize = False
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if st.session_state.pending_reset:
    for i in range(28):
        st.session_state[f"v{i+1}"] = 0.0
    st.session_state.prediction_result = None
    st.session_state.pending_reset = False

if st.session_state.pending_randomize:
    for i in range(28):
        # PCA-transformed credit card data centers around N(0, 1.2)
        st.session_state[f"v{i+1}"] = round(random.gauss(0, 1.2), 4)
    st.session_state.prediction_result = None
    st.session_state.pending_randomize = False

for i in range(28):
    if f"v{i+1}" not in st.session_state:
        st.session_state[f"v{i+1}"] = 0.0


def format_idr(value: float) -> str:
    """Indonesian thousand-separator format: 1.785.000"""
    return "{:,.0f}".format(value).replace(",", ".")


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow"><span class="indicator"></span>&nbsp;Model Active &mdash; XGBoost v1 / ONNX Runtime</div>
    <div class="hero-title">Fraud<span class="accent">Shield</span> Detection Console</div>
    <div class="hero-sub">Submit a transaction payload to receive a real-time risk assessment powered by a trained XGBoost model served via ONNX runtime.</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──────────────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
s1.markdown('<div class="stat-card"><span class="stat-val">284,807</span><span class="stat-lbl">Training Samples</span></div>', unsafe_allow_html=True)
s2.markdown('<div class="stat-card"><span class="stat-val">0.9995</span><span class="stat-lbl">ROC-AUC Score</span></div>', unsafe_allow_html=True)
s3.markdown('<div class="stat-card"><span class="stat-val">XGBoost</span><span class="stat-lbl">Base Algorithm</span></div>', unsafe_allow_html=True)
s4.markdown('<div class="stat-card"><span class="stat-val">&lt; 10ms</span><span class="stat-lbl">Avg. Inference Time</span></div>', unsafe_allow_html=True)

st.write("")

# ── Main layout ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown('<div class="panel"><div class="panel-title">Transaction Details</div>', unsafe_allow_html=True)

    if "amount_raw" not in st.session_state:
        st.session_state.amount_raw = 785_000.0
    if "amount_field" not in st.session_state:
        st.session_state.amount_field = format_idr(785_000.0)

    def on_amount_change():
        raw_str = st.session_state.amount_field.replace(".", "").replace(",", "").strip()
        try:
            parsed = float(raw_str)
            clamped = max(0.0, min(parsed, 500_000_000.0))
            st.session_state.amount_raw = clamped
            st.session_state.amount_field = format_idr(clamped)
        except ValueError:
            st.session_state.amount_field = format_idr(st.session_state.amount_raw)

    st.text_input(
        "Transaction Amount (IDR)",
        key="amount_field",
        on_change=on_amount_change,
        help="Digits only — dots are added live as you type."
    )
    transaction_amount = st.session_state.amount_raw

    # st.markdown scripts run in the main Streamlit document — no iframe needed,
    # making this compatible with all Streamlit versions.
    st.markdown("""
    <script>
    (function attach() {
        var inputs = document.querySelectorAll('input[type="text"]');
        var target = null;
        for (var i = 0; i < inputs.length; i++) {
            var wrap = inputs[i].closest('[data-testid="stTextInput"]');
            if (wrap && wrap.innerText.toLowerCase().includes('transaction amount')) {
                target = inputs[i];
                break;
            }
        }
        if (!target) { setTimeout(attach, 300); return; }
        if (target._idrAttached) return;
        target._idrAttached = true;

        target.addEventListener('input', function () {
            if (this._busy) return;
            this._busy = true;
            var raw = this.value.replace(/[^0-9]/g, '');
            if (raw !== '') {
                var formatted = parseInt(raw, 10).toLocaleString('id-ID');
                var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(this, formatted);
                this.dispatchEvent(new Event('input', { bubbles: true }));
            }
            this._busy = false;
        });
    })();
    </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # PCA Feature grid
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    title_col, rand_col, reset_col = st.columns([5, 2, 2])
    with title_col:
        st.markdown('<div class="panel-title">PCA Feature Vector &mdash; V1 through V28</div>', unsafe_allow_html=True)
    with rand_col:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("Randomize", key="randomize_btn", use_container_width=True):
            st.session_state.pending_randomize = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with reset_col:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("Reset", key="reset_btn", use_container_width=True):
            st.session_state.pending_reset = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    grid = [g1, g2, g3, g4]
    for i in range(28):
        with grid[i % 4]:
            st.number_input(
                f"V{i+1}",
                min_value=-30.0,
                max_value=30.0,
                step=0.01,
                format="%.4f",
                key=f"v{i+1}"
            )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Analyze Transaction", key="submit_btn", use_container_width=True):
        feature_vector = [st.session_state[f"v{i+1}"] for i in range(28)]
        api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/predict_transaction")

        with st.spinner("Running inference..."):
            try:
                t0 = time.time()
                response = requests.post(
                    api_url,
                    json={"features_v": feature_vector, "amount": transaction_amount},
                    timeout=10
                )
                latency_ms = round((time.time() - t0) * 1000, 1)
                response.raise_for_status()
                result_payload = response.json()
                result_payload["_latency_ms"] = latency_ms
                st.session_state.prediction_result = result_payload
            except requests.exceptions.ConnectionError:
                st.session_state.prediction_result = {
                    "error": "connection",
                    "detail": "Cannot reach API at http://127.0.0.1:8000. Is the FastAPI backend running?"
                }
            except requests.exceptions.HTTPError as exc:
                st.session_state.prediction_result = {"error": "http", "detail": str(exc)}
            except Exception as exc:
                st.session_state.prediction_result = {"error": "unknown", "detail": str(exc)}

        st.rerun()


# ── Result panel ───────────────────────────────────────────────────────────────
with right_col:
    result = st.session_state.prediction_result

    st.markdown('<div class="panel"><div class="panel-title">Risk Assessment</div>', unsafe_allow_html=True)

    if result is None:
        st.markdown("""
        <div class="awaiting-state">
            <div class="awaiting-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                     stroke="#3d5068" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="awaiting-title">Awaiting submission</div>
            <div class="awaiting-sub">Enter a feature vector and click Analyze Transaction.</div>
        </div>
        """, unsafe_allow_html=True)

    elif "error" in result:
        st.error(f"**Connection Failed** — {result['detail']}")

    else:
        is_fraud   = result["prediction"] == "FRAUD"
        fraud_prob = result["confidence_score"]
        fraud_pct  = round(fraud_prob * 100, 2)
        latency    = result.get("_latency_ms", "N/A")

        if is_fraud:
            st.markdown(f"""
            <div class="result-fraud">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
                     stroke="#f87171" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                     style="margin-bottom:0.5rem">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                <div class="result-heading-fraud">Fraud Detected</div>
                <div class="result-sub">Transaction exhibits high-risk signal patterns.</div>
                <div class="bar-track"><div class="bar-fraud" style="width:{fraud_pct}%"></div></div>
                <div class="score-number fraud">{fraud_pct}%</div>
                <div class="score-label">Fraud Probability</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            safe_pct = round((1 - fraud_prob) * 100, 2)
            st.markdown(f"""
            <div class="result-safe">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
                     stroke="#34d399" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                     style="margin-bottom:0.5rem">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <polyline points="9 12 11 14 15 10"/>
                </svg>
                <div class="result-heading-safe">Transaction Safe</div>
                <div class="result-sub">No significant fraud signals detected.</div>
                <div class="bar-track"><div class="bar-safe" style="width:{safe_pct}%"></div></div>
                <div class="score-number safe">{safe_pct}%</div>
                <div class="score-label">Legitimacy Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        details = result.get("details", {})
        # Use the amount that was actually analyzed from the result, 
        # falling back to current if for some reason it's missing.
        analyzed_amount = details.get("raw_amount", transaction_amount)

        st.markdown(f"""
        <div style="margin-top:1.25rem;">
            <span class="pill"><span class="pill-lbl">Latency</span><strong>{latency} ms</strong></span>
            <span class="pill"><span class="pill-lbl">Amount</span><strong>IDR {format_idr(analyzed_amount)}</strong></span>
            <span class="pill"><span class="pill-lbl">Model</span><strong>{details.get('model_version', 'v1_xgboost_onnx')}</strong></span>
            <span class="pill"><span class="pill-lbl">Score</span><strong>{fraud_prob:.6f}</strong></span>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        with st.expander("Raw API Response"):
            st.json({k: v for k, v in result.items() if k != "_latency_ms"})

    st.markdown('</div>', unsafe_allow_html=True)
