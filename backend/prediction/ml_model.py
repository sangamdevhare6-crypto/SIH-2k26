import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "rainfall_model.pkl")
encoder_path = os.path.join(BASE_DIR, "risk_encoder.pkl")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)


def predict_risk(rainfall, temperature, humidity, wind_speed, pressure):

    features = pd.DataFrame(
        [[rainfall, temperature, humidity, wind_speed, pressure]],
        columns=[
            "rainfall",
            "temperature",
            "humidity",
            "wind_speed",
            "pressure"
        ]
    )

    prediction = model.predict(features)

    risk_level = encoder.inverse_transform(prediction)[0]

    return risk_level