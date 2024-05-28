import cv2 
import numpy as np
import tensorflow as tf
from schemas.emotion_schema import GetEmotionPercentagesResponse

# Function to load the pre-trained emotion detection model
def load_model():
    model = tf.keras.models.load_model("models/model2/model2.h5")
    return model

# Function to load the Haar cascade classifier for face detection
def load_face_cascade():
    haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(haar_file)
    return face_cascade

# Function to extract features from an image for prediction
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    feature = feature / 255.0
    return feature

# Function to predict emotion probabilities using the loaded model
def predict_emotion(model, img):
    pred = model.predict(img)
    return pred

# Function to calculate the percentage of each emotion in the predictions list
def getPercentages(predictions):
    # Initialize a dictionary to store the count of each emotion
    emotion_count_map = {
        'Angry': 0,
        'Disgusted': 0,
        'Fearful': 0,
        'Happy': 0,
        'Neutral': 0,
        'Sad': 0,
        'Surprised': 0
    }
    
    # Count the occurrences of each emotion in the predictions list
    for prediction in predictions:
        if prediction in emotion_count_map:
            emotion_count_map[prediction] += 1

    # Calculate the total number of predictions
    total_predictions = len(predictions)
    
    # Calculate the percentage of each emotion
    percentages = {emotion: round((count / total_predictions * 100), 2) for emotion, count in emotion_count_map.items()}
    return percentages

# Function to process emotions from a video
def process_video_emotions(video_path):
    # Load the pre-trained model and face cascade classifier
    model = load_model()
    face_cascade = load_face_cascade()
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Initialize an empty list to store emotion predictions
    predictions = []
    
    # Process each frame of the video
    while True:
        # Read a frame from the video
        ret, frame = video.read()
        
        # Break the loop if there are no more frames
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Process each detected face in the frame
        for (x, y, w, h) in faces:
            # Extract the face region and resize it
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (48, 48))
            
            # Extract features and make predictions
            face = extract_features(face)
            prediction = predict_emotion(model, face)
            
            # Get the index of the predicted emotion
            predicted_emotion = np.argmax(prediction)
            
            # Add the predicted emotion to the list of predictions
            predictions.append(predicted_emotion)
    
    # Calculate percentages of each emotion
    percentages = getPercentages(predictions)
    
    # Create and return a response object containing the percentages
    return GetEmotionPercentagesResponse(
        Angry=percentages['Angry'], 
        Disgusted=percentages['Disgusted'], 
        Fearful=percentages['Fearful'], 
        Happy=percentages['Happy'], 
        Neutral=percentages['Neutral'], 
        Sad=percentages['Sad'], 
        Surprised=percentages['Surprised']
    )
