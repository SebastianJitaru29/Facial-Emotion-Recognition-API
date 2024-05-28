from flask import Flask, request
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model("emotiondetector_h5/emotiondetector.h5")

# Define emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

@app.route('/predict_emotion', methods=['POST'])
def predict_emotion():
    # Receive image
    file = request.files['image']
    
    # Read image
    img = Image.open(file).convert("L")  # Open in black and white
    img = img.resize((48, 48))  # Resize image to desired size

    # Convert image to array and normalize
    img_array = np.array(img) / 255.0

    # Expand dimensions to match the input shape expected by the model
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    predictions = model.predict(img_array)

    # Get the index of the highest probability
    predicted_class_index = np.argmax(predictions[0])

    # Get the predicted emotion
    predicted_emotion = emotion_labels[predicted_class_index]

    # Return predicted emotion
    return predicted_emotion

if __name__ == '__main__':
    app.run(debug=True)
