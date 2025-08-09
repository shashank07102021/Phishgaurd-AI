import streamlit as st
import joblib
import re

# Load model
model = joblib.load('phishing_model.pkl')

# Feature extraction function
def has_ip(url):
    ip_pattern = r'((\d{1,3}\.){3}\d{1,3})'
    return bool(re.search(ip_pattern, url))

def extract_features(url):
    features = {
        'url_length': len(url),
        'has_at': '@' in url,
        'has_dash': '-' in url,
        'has_https': 'https' in url,
        'digit_count': sum(char.isdigit() for char in url),
        'has_ip': has_ip(url)
    }
    return list(features.values())

# Streamlit UI
st.title("PhishGuard AI - URL Phishing Detector")
st.markdown("🔐 Enter a URL to check if it's **phishing or legitimate**.")

# Input URL
url = st.text_input("Enter URL here:")

if st.button("Predict"):
    if url:
        features = extract_features(url)
        prediction = model.predict([features])[0]
        result = "🛑 Phishing URL" if prediction == 1 else "✅ Legitimate URL"
        st.markdown(f"### Prediction: {result}")
    else:
        st.warning("⚠️ Please enter a URL first.")


