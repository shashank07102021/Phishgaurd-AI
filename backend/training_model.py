import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
data = pd.read_csv('phishing_dataset.csv')

# Separate features and label
X = data.drop('label', axis=1)
y = data['label']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Ensure features are numeric
X_train = X_train.apply(pd.to_numeric, errors='coerce')
X_train = X_train.fillna(0)

X_test = X_test.apply(pd.to_numeric, errors='coerce')
X_test = X_test.fillna(0)
# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'phishing_model.pkl')
print("Model saved as phishing_model.pkl")