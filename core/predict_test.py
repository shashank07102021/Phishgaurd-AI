import joblib
import pandas as pd
from feature_extractor import extract_features

# Load the trained model
model = joblib.load('backend/phishing_model.pkl')

# URL to test
url = "http://192.168.0.1/login"

# Extract features (returns a dictionary of numerical features)
features = extract_features(url)

# These must match the order used during model training
feature_names = ['url_length', 'has_at', 'has_dash', 'has_https', 'digit_count', 'has_ip','is_shortened','suspicious_tld','url_entropy','count_subdomains','contains_keywords']

# Convert to DataFrame in correct order
input_data = pd.DataFrame([[features[feature] for feature in feature_names]], columns=feature_names)

# Make prediction
prediction = model.predict(input_data)


# Output result
if prediction[0] == 1:
    print("⚠️  This is a phishing URL.")
else:
    print("✅  This is a legitimate URL.")