import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv('phishing_dataset.csv')  # Your dataset with 'url' column

# Define only the feature columns to use
features = ['url_length', 'has_at', 'has_dash', 'has_https', 'digit_count', 'has_ip']
X = df[features]  # ✅ Only include the features (not 'url')
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, 'backend/phishing_model.pkl')
print("Model saved as phishing_model.pkl")