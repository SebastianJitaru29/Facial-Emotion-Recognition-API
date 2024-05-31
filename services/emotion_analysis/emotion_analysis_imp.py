
from schemas.emotion_schema import GetEmotionPercentagesResponse
from services.emotion_analysis.emotion_analysis_service import EmotionsAnalysisService
from utils.utils import load_model, load_face_cascade, extract_features, predict_emotion, getPercentages 
import cv2

class EmotionsAnalysisImp(EmotionsAnalysisService):
    def __init__(self, model_path: str):
        self.model = load_model(model_path)
        self.face_cascade = load_face_cascade()

    def get_emotion_percentages(self, video_path: str) -> GetEmotionPercentagesResponse:
            """
            Calculates the percentages of different emotions detected in a video.

            Args:
                video_path (str): The path to the video file.

            Returns:
                GetEmotionPercentagesResponse: An object containing the percentages of each emotion detected.
            """
            predictions = []
            labels = {0: 'Angry', 1: 'Disgusted', 2: 'Fearful', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprised'}
            # Load the video with path or 0 for webcam
            video = cv2.VideoCapture(video_path)
            while True:
                ret, im = video.read()
                if not ret:
                    break
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(im, 1.3, 5)
                try:
                    for (p, q, r, s) in faces:
                        image = gray[q:q + s, p:p + r]
                        cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
                        image = cv2.resize(image, (48, 48))
                        img = extract_features(image)
                        pred = predict_emotion(self.model, img)
                        prediction_label = labels[pred.argmax()]
                        predictions.append(prediction_label)
                        cv2.putText(im, prediction_label, (p, q - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    cv2.imshow('Emotion Detector', im)
                    if cv2.waitKey(1) == 27:
                        break
                except cv2.error:
                    pass
            video.release()
            cv2.destroyAllWindows()
            percentages = getPercentages(predictions)
            return GetEmotionPercentagesResponse(Angry=percentages['Angry'], Disgusted=percentages['Disgusted'], Fearful=percentages['Fearful'], Happy=percentages['Happy'], Neutral=percentages['Neutral'], Sad=percentages['Sad'], Surprised=percentages['Surprised'])
