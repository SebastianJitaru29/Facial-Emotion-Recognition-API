import cv2
import numpy as np
import tensorflow as tf
import os
import shutil
    

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

#Delete /static/videos/ content
def delete_video(video_name):
    folder = "static/videos/"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))