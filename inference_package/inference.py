import joblib
import os
import pandas as pd
from io import StringIO

def model_fn(model_dir):
    # Called ONCE, when the container starts up
    return joblib.load(os.path.join(model_dir, "model.joblib"))

def input_fn(request_body, content_type="text/csv"):
    # Called on EVERY prediction request, to parse the incoming payload
    if content_type == "text/csv":
        return pd.read_csv(StringIO(request_body), header=None)
    raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(input_data, model):
    # Called on EVERY prediction request, after input_fn
    return model.predict_proba(input_data)[:, 1]

def output_fn(prediction, accept="text/csv"):
    # Called on EVERY prediction request, to format the response
    return ",".join(map(str, prediction)), accept