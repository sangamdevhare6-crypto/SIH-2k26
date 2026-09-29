import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


# Load dataset
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "rainfall_data.csv"
)

data = pd.read_csv(DATASET_PATH)


# Input features
X = data[
    [
        "rainfall",
        "temperature",
        "humidity",
        "wind_speed",
        "pressure"
    ]
]


# Target
y = data["risk"]


# Convert risk names to numbers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Test
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("================================")
print("RainGuard AI ML Model")
print("================================")

print("Model trained successfully!")

print("Accuracy:", accuracy)

print("================================")


# Save model
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

joblib.dump(
    model,
    os.path.join(MODEL_DIR, "rainfall_model.pkl")
)


# Save encoder
joblib.dump(
    encoder,
    os.path.join(MODEL_DIR, "risk_encoder.pkl")
)


print("rainfall_model.pkl created!")
print("risk_encoder.pkl created!")