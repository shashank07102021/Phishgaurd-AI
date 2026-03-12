from  feature_extractor import extract_features

phishing_url = "http://192.168.0.1/login/verify@paypal.com"

legit_url = "https://www.google.com"

print("Phishing Url Features:")
print(extract_features(phishing_url))

print("legit Url Features:")
print(extract_features(legit_url))