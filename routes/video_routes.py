from flask import Blueprint, request, jsonify
import logging
from services.data.firebase_imp import FirebaseImp
from services.emotion_analysis.emotion_analysis_imp import EmotionsAnalysisImp
import requests

video_routes = Blueprint("video_routes", __name__)

# Initialize Firebase service
firebase_cred_path = "firebase/backend-testing-tfg-firebase-adminsdk-vx45t-d0c10e29bd.json"
storage_bucket = "backend-testing-tfg.appspot.com"
firebase_service = FirebaseImp(firebase_cred_path=firebase_cred_path, storage_bucket=storage_bucket)

logger = logging.getLogger(__name__)

def download_and_analyze_video(video_name):
    # Download the video from Firebase Storage
    logger.info(f"Attempting to download video: {video_name} from storage.")
    try:
        video_path = firebase_service.download_video_from_storage(video_name)
        logger.info(f"Video downloaded successfully to: {video_path}")
    except Exception as e:
        logger.error(f"Failed to download video: {e}")
        return

    # Perform emotion analysis on the downloaded video
    logger.info("Initializing emotion analysis.")
    emotion_analysis_service = EmotionsAnalysisImp(model_path="models/model2/model2.h5")
    try:
        result = emotion_analysis_service.get_emotion_percentages(video_path)
        logger.info(f"Emotion analysis result: {result}")
    except Exception as e:
        logger.error(f"Failed to analyze video: {e}")
        return
    result_dict = result if isinstance(result, dict) else result.__dict__    # Upload the analysis results to Firestore
    logger.info("Uploading analysis results to Firestore.")
    try:
        doc_id = firebase_service.upload_to_firestore(result_dict)
        logger.info(f"Analysis results uploaded successfully. Document ID: {doc_id}")
    except Exception as e:
        logger.error(f"Failed to upload analysis results to Firestore: {e}")


@video_routes.route("/process_video", methods=["POST"])
def process_video():
    # Assuming the request contains the name of the video to process
    video_name = request.json.get("video_name")
    if not video_name:
        return jsonify({"error": "Video name is missing in the request"}), 400
    # Process the video

    download_and_analyze_video(video_name)
    return jsonify({"message": "Video processing initiated"}), 200

@video_routes.route("/test", methods=["GET"])
def call_hello_world():
    logger.info("Attempting to call test firebase function.")
    firebase_funcion_url = "https://europe-west1-backend-testing-tfg.cloudfunctions.net/hello_world"
    try: 
        response = requests.get(firebase_funcion_url) #Allows to call the firebase function hosted elswhere
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to call firebase function"}), response.status_code
    except Exception as e:
        logger.error(f"Failed to call firebase function: {e}")
        return jsonify({"error": "Failed to call firebase function"}), 500