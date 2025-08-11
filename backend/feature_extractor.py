import csv
import re
import pandas as pd
from urllib.parse import urlparse
import math
from collections import Counter
# Function to check if the URL has an IP address

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
    suspicious_tlds = ["tk", "ga", "ml", "cf", "gq", "xyz", "top", "club"]
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


# Function to extract features from a URL
def extract_features(url):
    return {
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

# List of phishing and legitimate URLs
phishing_urls = [
    "http://paypal-login.com",
    "https://secure-google.com@fake.ru",
    "http://192.168.0.1/login",
    "http://verify-update-security.com",
    "http://paypal-update-login.com",
    "https://accounts.google.com",
    "https://secure-login.amazon.com@fakepage.ru",
    "http://ver1fy-your-bank.com",
    "https://secure-google-login.com@phishingsite.ru"
    ]

legit_urls = [
    "https://www.google.com",
    "https://www.bankofamerica.com",
    "https://www.github.com",
    "https://www.amazon.com",
    "https://www.instagram.com"

]

# Prepare dataset
data = []

# Label phishing URLs as 1
for url in phishing_urls:
   features = extract_features(url)
features['label'] = 1  # phishing
data.append(features)

# Label legit URLs as 0
for url in legit_urls:
    features = extract_features(url)
    features['label'] = 0
    data.append(features)

# Write to CSV file
with open('phishing_dataset.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print("Dataset saved successfully as phishing_dataset.csv")