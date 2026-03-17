import pickle
import pandas as pd


# importing the model
try:
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# model version
MODEL_VERSION = "1.0.0"

# get clsass labels from model
class_labels = model.classes_.tolist()


def predict_output(user_input):
    df = pd.DataFrame([user_input])
    # predict class
    prediction = model.predict(df)[0]
    # Get the predicted class label
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # create mapping: (class_name: probability)
    class_proba = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": prediction,
        "confidence": round(confidence, 4),
        "class_probabilities": class_proba,
    }
