import joblib
import pandas as pd
from feature_extractor import extract_features

# Load the trained model
model = joblib.load("backend/phishing_model.pkl")

# Example URL to test
url = "http://paypal-login.com"

# Extract features from the URL
features = extract_features(url)

# Convert features to DataFrame
X_test = pd.DataFrame([features])

# Make prediction
prediction = model.predict(X_test)

# Display result
if prediction[0] == 1:
    print("⚠️ Phishing URL detected!")
else:
    print("✅ Legitimate URL.")