from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import ChatOllama
from PIL import Image
import collections
import tensorflow as tf
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

collections.Iterable = collections.abc.Iterable
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
CORS(app)

router_agent = ChatOllama(model="llama3.2")

try:
    crop_model = joblib.load('recommend.pkl')
    print("Crop Model: ",crop_model)
    print("✅ Crop recommendation model loaded.")
except Exception as e:
    print(f"⚠️ Failed to load recommend.pkl: {e}")
    crop_model = None

try:
    disease_model = tf.keras.models.load_model("PlantDisease(5).h5")
    print("✅ Plant disease model loaded.")
except Exception as e:
    print(f"⚠️ Failed to load PlantDisease(5).h5: {e}")
    disease_model = None

CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

def preprocess_image(file):
    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    return img_array

def route_with_llm(user_input, has_image=False):
    """LLM decides whether to use crop or disease model."""
    if has_image:
        return "plant_disease"

    system_prompt = (
        "You are an expert routing assistant for an agriculture AI.\n"
        "Respond with exactly one of these two words only:\n"
        "- crop_recommendation\n"
        "- plant_disease\n\n"
        "Rules:\n"
        "- If query includes soil, fertilizer, N, P, K, temperature, humidity, rainfall → crop_recommendation\n"
        "- If query mentions leaf, yellow spots, disease, infection, or image → plant_disease\n"
    )

    try:
        response = router_agent.invoke(f"{system_prompt}\nUser: {user_input}")
        decision = response.content.strip().lower()
        if "disease" in decision:
            return "plant_disease"
        return "crop_recommendation"
    except Exception as e:
        print(f"⚠️ Router LLM failed: {e}")
        return "crop_recommendation"

def recommend_crop(data):
    try:
        N = float(data.get("N", 0))
        P = float(data.get("P", 0))
        K = float(data.get("K", 0))
        temperature = float(data.get("temperature", 0))
        humidity = float(data.get("humidity", 0))

        features = np.array([[N, P, K, temperature, humidity]])
        prediction = crop_model.predict(features)
        crop = str(prediction[0])
        return {"recommended_crop": crop}
    except Exception as e:
        return {"error": f"Crop recommendation failed: {e}"}

def classify_disease(file):
    try:
        img = preprocess_image(file)
        predictions = disease_model.predict(img)
        predicted_class = CLASS_NAMES[int(np.argmax(predictions))]
        confidence = float(np.max(predictions))
        return {"predicted_disease": predicted_class, "confidence": confidence}
    except Exception as e:
        return {"error": f"Disease classification failed: {e}"}

@app.route("/agent", methods=["POST"])
def ai_agent():
    try:
        has_image = "file" in request.files
        content_type = request.content_type or ""
        user_query = ""

        # Safely handle both JSON and multipart/form-data
        if "application/json" in content_type:
            data = request.get_json() or {}
            print("Data: ",data)
            user_query = data.get("query", "")
            print("User query: ",user_query)
        else:
            user_query = request.form.get("query", "")
            print("User query: ",user_query)
            data = request.form or {}
            print("Data: ",data)

        if not user_query and not has_image:
            return jsonify({"error": "No query or image provided"}), 400

        decision = route_with_llm(user_query, has_image)
        print(f"🤖 Routing decision: {decision}")

        if decision == "crop_recommendation":
            if crop_model is None:
                return jsonify({"error": "Crop model not loaded"}), 500
            result = recommend_crop(data)
        else:
            if disease_model is None:
                return jsonify({"error": "Disease model not loaded"}), 500
            file = request.files["file"]
            print("File received:", file.filename)
            result = classify_disease(file)

        result["model_used"] = decision
        return jsonify(result)

    except Exception as e:
        print("❌ Error in /agent:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3001)