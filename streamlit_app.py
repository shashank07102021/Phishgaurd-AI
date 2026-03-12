import streamlit as st
import joblib
import sys
sys.path.append('D:/Phishgaurd AI/core')
from feature_extractor import extract_features
import re
import math
from collections import Counter
from urllib.parse import urlparse
from utils.emailer import send_email_alert
from utils.email_template import phishing_alert_html, defang

# Load model
model = joblib.load('D:/Phishgaurd AI/core/phishing_model.pkl')




# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PhishGuard AI", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0b0f14;
}

/* Headings */
h1, h2, h3 {
    color: #e5e7eb;
}

/* Panels */
.panel {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 20px;
    margin-top: 18px;
}

/* Status panels */
.status-neutral { background:#020617; }
.status-safe { background:#064e3b; }
.status-danger { background:#7f1d1d; }

/* Muted text */
.muted {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 4px;
}

/* Tagline */
.tagline {
    font-size: 12px;
    color: #f87171;
    letter-spacing: 0.12em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="padding:20px 0;">
    <div class="tagline">SECURITY ANALYSIS SYSTEM</div>
    <h1>PhishGuard AI</h1>
    <p class="muted">Detect → Observe → Preserve Evidence → Act</p>
</div>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------
tabs = st.tabs(["🔗 URL Scan", "🖼 Image Scan", "📄 PDF Scan", "📁 Incidents", "ℹ️ About"])

# ================= URL SCAN TAB =================
with tabs[0]:

    # ---- INPUT PANEL ----
    st.markdown("""
    <div class="panel">
        <h3>URL Phishing Scan</h3>
        <p class="muted">Analyze a URL before opening it.</p>
    </div>
    """, unsafe_allow_html=True)

    url = st.text_input("Target URL", placeholder="https://example.com")
    scan_btn = st.button("🔍 Scan URL")

    # ---- SCAN RESULT PANEL ----
    if not scan_btn:
        st.markdown("""
        <div class="panel status-neutral">
            <h3>Scan Status</h3>
            <p class="muted">
                No scan performed yet.<br>
                System awaiting URL analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        if not url or not url.strip():
            st.error("⚠️ Please enter a URL before scanning.")
        elif not url.startswith("http://") and not url.startswith("https:"):
            st.error("Invalid URL . Must start with http://  or https://")
        else:
            features = extract_features(url)
            probs = model.predict_proba([features])[0]
            legit_p, phish_p = float(probs[0]), float(probs[1])

            threshold = 0.60
            is_phishing = phish_p >= threshold
            confidence = max(legit_p, phish_p) * 100

            state_class = "status-danger" if is_phishing else "status-safe"
            verdict = "LIKELY PHISHING" if is_phishing else "LIKELY SAFE"

            st.markdown(f"""
            <div class="panel {state_class}">
                <h3>{verdict}</h3>
                <p class="muted">
                    Confidence: {confidence:.2f}%<br>
                    Incident ID: PG-{hash(url) % 100000}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---- ACTIONS ----
    st.markdown("""
    <div class="panel">
        <h3>Incident Actions</h3>
        <p class="muted">Available after confirmed detection.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.button("🛡 Safe Preview", disabled=True)
    with c2:
        st.button("📄 View Evidence", disabled=True)
    with c3:
        st.button("📑 Forensic Report", disabled=True)
    with c4:
        st.button("🚨 Report to Cyber Cell", disabled=True)

    # ---- EXPLAINABILITY ----
    with st.expander("Why was this flagged?"):
        st.markdown("""
        **Signals**
        - URL structure
        - HTTPS usage
        - IP-based patterns
        - Keyword presence
        - Entropy & obfuscation

        **Threshold**
        - Default: 0.60

        **Note**
        - Statistical system
        - False positives and negatives are possible
        """)
