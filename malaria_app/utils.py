# malaria_app/utils.py

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

def load_malaria_model():
    # Chemin absolu vers le modèle
    model_path = os.path.join(settings.BASE_DIR, 'malaria_app', 'models', 'best_model_malaria_cnn.h5')
    return load_model(model_path)
import os
from django.conf import settings
# malaria_app/utils.py
def predict_malaria(image_path):
    model = load_malaria_model()
    
    img = cv2.imread(image_path)
    img = cv2.resize(img, (50, 50))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img)[0]
    class_idx = np.argmax(prediction)
    confidence = float(prediction[class_idx])
    classes = ["Uninfected", "Parasitized"]
    
    return {
        'class': classes[class_idx],
        'confidence': confidence
    }