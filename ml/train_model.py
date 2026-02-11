import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Paths
DATA_PATH = r'D:\FraudDetectionSystem\data\creditcard.csv'
MODEL_PATH = r'D:\FraudDetectionSystem\ml\fraud_model.pkl'

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Load dataset
data = pd.read_csv(DATA_PATH)

# Features and target
X = data.drop(['Class'], axis=1)
y = data['Class']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model
joblib.dump(clf, MODEL_PATH)
print(f"Model trained and saved as {MODEL_PATH}")
