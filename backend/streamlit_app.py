import streamlit as st
import joblib
import re
import math
from collections import Counter
from urllib.parse import urlparse
# Load model
model = joblib.load('phishing_model.pkl')

# Feature extraction function
def has_ip(url):
    ip_pattern = r'((\d{1,3}\.){3}\d{1,3})'
    return bool(re.search(ip_pattern, url))

# Detect shortened URLs
def is_shortened(url):
    shortened_domains = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "buff.ly", "adf.ly"]
    return any(short in url for short in shortened_domains)

# Detect suspicious TLD
def suspicious_tld(url):
    suspicious_tlds = ["tk", "ga", "ml", "cf", "gq", "xyz", "top", "club","Fun"]
    domain = urlparse(url).netloc.lower()
    return any(domain.endswith("." + tld) for tld in suspicious_tlds)

# Calculate URL entropy
def url_entropy(url):
    probs = [freq / len(url) for freq in Counter(url).values()]
    return -sum(p * math.log2(p) for p in probs)

# Count subdomains
def count_subdomains(url):
    domain = urlparse(url).netloc
    return domain.count(".")

# Detect phishing keywords
def contains_keywords(url):
    keywords = ["login", "verify", "secure", "account", "update", "free", "win", "bank"]
    return any(keyword in url.lower() for keyword in keywords)

# Main feature extraction
def extract_features(url):
    features = {
        'url_length': len(url),
        'has_at': '@' in url,
        'has_dash': '-' in url,
        'has_https': 'https' in url,
        'digit_count': sum(char.isdigit() for char in url),
        'has_ip': has_ip(url),
        'is_shortened': is_shortened(url),
        'suspicious_tld': suspicious_tld(url),
        'url_entropy': url_entropy(url),
        'count_subdomains': count_subdomains(url),
        'contains_keywords': contains_keywords(url)
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


