import cv2
import numpy as np
import tensorflow as tf

def load_model(model_path: str):
    return tf.keras.models.load_model(model_path)

def load_face_cascade():
    haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    return cv2.CascadeClassifier(haar_file)

def extract_features(image):
    feature = np.array(image).reshape(1, 48, 48, 1) / 255.0
    return feature

def predict_emotion(model, img):
    return model.predict(img)

def getPercentages(predictions):
    emotion_count_map = {emotion: 0 for emotion in ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']}
    for prediction in predictions:
        emotion_count_map[prediction] += 1
    percentages = {emotion: round((count / len(predictions) * 100), 2) for emotion, count in emotion_count_map.items()}
    return percentages
