import sqlite3
from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from models.predict import predict_disease
from database import save_prediction, get_predictions
from pdf_report import generate_pdf

treatments = {
    "Pepper Bell - Bacterial Spot": "Remove infected leaves and use copper-based bactericide spray.",

    "Pepper Bell - Healthy": "Plant is healthy. Continue regular care and monitoring.",

    "Potato - Early Blight": "Remove infected leaves and apply suitable fungicide. Avoid overhead watering.",

    "Potato - Healthy": "Plant is healthy. Maintain proper irrigation and nutrition.",

    "Potato - Late Blight": "Remove infected plants and apply recommended fungicide immediately.",

    "Tomato - Bacterial Spot": "Remove infected leaves and apply copper-based spray.",

    "Tomato - Early Blight": "Remove affected leaves and use fungicide treatment.",

    "Tomato - Healthy": "Plant is healthy. Continue normal care.",

    "Tomato - Late Blight": "Remove infected parts and apply fungicide. Avoid excess moisture.",

    "Tomato - Leaf Mold": "Improve air circulation and apply appropriate fungicide.",

    "Tomato - Mosaic Virus": "Remove infected plants and control insect vectors.",

    "Tomato - Septoria Leaf Spot": "Remove infected leaves and apply fungicide.",

    "Tomato - Spider Mites": "Use insecticidal soap or recommended miticide spray.",

    "Tomato - Target Spot": "Remove infected leaves and apply fungicide.",

    "Tomato - Yellow Leaf Curl Virus": "Control whiteflies and remove infected plants.",

    "Tomato - Two Spotted Spider Mite": "Spray recommended miticide and maintain proper plant moisture."
}
disease_info = {

    "Tomato - Two Spotted Spider Mite": {
        "symptoms": "Yellow spots on leaves, leaf damage, and possible web formation.",
        "prevention": "Maintain proper humidity, remove infected leaves, and control mites."
    },

    "Tomato - Early Blight": {
        "symptoms": "Brown circular spots with yellow rings on leaves.",
        "prevention": "Use healthy seeds, avoid wet leaves, and apply fungicide."
    },

    "Tomato - Late Blight": {
        "symptoms": "Dark lesions on leaves and rapid plant damage.",
        "prevention": "Avoid excess moisture and remove infected plants."
    }
}
all_diseases = {

    "Pepper Bell - Bacterial Spot": {
        "symptoms": "Dark spots on leaves and fruit.",
        "causes": "Bacterial infection caused by Xanthomonas.",
        "prevention": "Use clean seeds and avoid excess moisture.",
        "treatment": "Remove infected leaves and use copper spray."
    },

    "Potato - Early Blight": {
        "symptoms": "Brown spots with yellow rings on leaves.",
        "causes": "Fungal infection.",
        "prevention": "Use healthy seeds and proper crop rotation.",
        "treatment": "Apply recommended fungicide."
    },

    "Potato - Late Blight": {
        "symptoms": "Dark lesions on leaves and stems.",
        "causes": "Fungal-like pathogen infection.",
        "prevention": "Avoid excess moisture.",
        "treatment": "Remove infected parts and apply fungicide."
    },

    "Tomato - Early Blight": {
        "symptoms": "Brown circular spots on leaves.",
        "causes": "Alternaria fungal infection.",
        "prevention": "Maintain plant hygiene.",
        "treatment": "Use suitable fungicide."
    },

    "Tomato - Two Spotted Spider Mite": {
        "symptoms": "Yellow spots, leaf damage, and web formation.",
        "causes": "Spider mite infestation.",
        "prevention": "Maintain humidity and monitor plants.",
        "treatment": "Use recommended miticide spray."
    }

}
app = Flask(__name__)
latest_prediction = {}

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/diseases")
def diseases():

    return render_template(
        "diseases.html",
        diseases=all_diseases
    )

@app.route("/history")
def history():

    records = get_predictions()

    return render_template(
        "history.html",
        records=records
    )

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No file selected"

    filename = secure_filename(file.filename)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    result, confidence = predict_disease(filepath)
    save_prediction(filename, result, confidence)
    global latest_prediction

    latest_prediction = {
    "image_path": filepath,
    "disease": result,
    "confidence": confidence,
    "treatment": treatments.get(result),
    "symptoms": disease_info.get(result, {}).get("symptoms"),
    "prevention": disease_info.get(result, {}).get("prevention")
}

    return render_template(
    "index.html",
    prediction=result,
    confidence=confidence,
    treatment=treatments.get(result),
    symptoms=disease_info.get(result, {}).get("symptoms"),
    prevention=disease_info.get(result, {}).get("prevention"),
    image_path=filepath
)
@app.route("/download-report")
def download_report():

    output_file = "Plant_Disease_Report.pdf"

    generate_pdf(
        latest_prediction["image_path"],
        latest_prediction["disease"],
        latest_prediction["confidence"],
        latest_prediction["treatment"],
        latest_prediction["symptoms"],
        latest_prediction["prevention"],
        output_file
    )

    return send_file(output_file, as_attachment=True)
@app.route("/analytics")
def analytics():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT disease, COUNT(*)
        FROM predictions
        GROUP BY disease
    """)

    data = cursor.fetchall()

    conn.close()

    diseases = []
    counts = []

    for row in data:
        diseases.append(row[0])
        counts.append(row[1])

    return render_template(
        "analytics.html",
        diseases=diseases,
        counts=counts
    )

if __name__ == "__main__":
    app.run(debug=True)