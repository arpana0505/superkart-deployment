
from flask import Flask, request, jsonify
import io
import joblib
import pandas as pd

superkart_api = Flask(__name__)

MODEL_PATH = "superkart_model.joblib"
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

@superkart_api.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@superkart_api.post("/v1/predict")
def predict():
    try:
        payload = request.get_json(force=True)
        input_df = pd.DataFrame([payload])

        missing_cols = [col for col in FEATURE_COLUMNS if col not in input_df.columns]
        if missing_cols:
            return jsonify({"error": f"Missing columns: {missing_cols}"}), 400

        prediction = model.predict(input_df[FEATURE_COLUMNS])[0]
        return jsonify({"prediction": float(prediction)}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

@superkart_api.post("/v1/predictbatch")
def predict_batch():
    try:
        if "file" not in request.files:
            return jsonify({"error": "CSV file is required using the key 'file'."}), 400

        uploaded_file = request.files["file"]
        batch_df = pd.read_csv(io.BytesIO(uploaded_file.read()))

        missing_cols = [col for col in FEATURE_COLUMNS if col not in batch_df.columns]
        if missing_cols:
            return jsonify({"error": f"Missing columns: {missing_cols}"}), 400

        predictions = model.predict(batch_df[FEATURE_COLUMNS])
        result = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(result), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
