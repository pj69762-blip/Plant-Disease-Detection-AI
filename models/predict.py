import numpy as np
from tensorflow.keras.models import load_model
from models.preprocess import preprocess_image
from models.labels import labels

model = load_model("models/plant_disease_model.keras")


def predict_disease(img_path):
    img = preprocess_image(img_path)

    prediction = model.predict(img)

    predicted_class = np.argmax(prediction)

    disease = labels[predicted_class]

    confidence = round(np.max(prediction) * 100, 2)

    return disease, confidence