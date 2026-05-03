import joblib
import pandas as pd

# Load artifacts
high_value_artifact = joblib.load("../models/high_value_model.pkl")
delay_artifact = joblib.load("../models/delay_model.pkl")

# Extract
high_value_model = high_value_artifact["model"]
high_value_threshold = high_value_artifact["threshold"]

delay_model = delay_artifact["model"]
delay_threshold = delay_artifact["threshold"]

high_value_columns = joblib.load("../models/high_value_columns.pkl")
delay_columns = joblib.load("../models/delay_columns.pkl")

import pandas as pd

def preprocess_input(input_dict, model_type):

    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)

    if model_type == "high_value":
        cols = high_value_columns
    else:
        cols = delay_columns

    # Create full DataFrame at once (FAST)
    df = df.reindex(columns=cols, fill_value=0)

    return df

def predict_high_value(input_dict):
    df = preprocess_input(input_dict, "high_value")
    
    prob = high_value_model.predict_proba(df)[:, 1]
    pred = (prob >= high_value_threshold).astype(int)
    
    return pred[0], prob[0]


def predict_delay(input_dict):
    df = preprocess_input(input_dict, "delay")
    
    prob = delay_model.predict_proba(df)[:, 1]
    pred = (prob >= delay_threshold).astype(int)
    
    return pred[0], prob[0]