import logging
import coloredlogs
from services.emotion_analysis.emotion_analysis_imp import EmotionsAnalysisImp
from services.data.firebase_imp import FirebaseImp

# Set up colored logs for better readability
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize the Firebase service once
firebase_cred_path = "firebase/backend-testing-tfg-firebase-adminsdk-vx45t-d0c10e29bd.json"
storage_bucket = "backend-testing-tfg.appspot.com"
logger.info(f"Initializing Firebase with credentials: {firebase_cred_path} and bucket: {storage_bucket}")
firebase_service = FirebaseImp(firebase_cred_path=firebase_cred_path, storage_bucket=storage_bucket)

def get_video_to_analyze(firebase_service):
    video_path = None
    try:
        video_path = firebase_service.download_video_from_storage()
        logger.info(f"Video downloaded successfully to: {video_path}")
    except Exception as e:
        logger.error(f"Failed to download video: {e}")
    
    return video_path

def analyze_video(video_path):
    logger.info(f"Initializing emotion analysis with model.")
    emotion_analysis_service = EmotionsAnalysisImp(model_path="models/model2/model2.h5")
    result = emotion_analysis_service.get_emotion_percentages(video_path)
    logger.info(f"Emotion analysis result: {result}")
    return result

def main():
    # Download the video to analyze
    video_path = get_video_to_analyze(firebase_service)
    if not video_path:
        logger.error("No video path found, exiting.")
        return
    
    # Perform emotion analysis on the video
    result = analyze_video(video_path)
    
    # Convert the result to a dictionary (if it isn't already)
    result_dict = result if isinstance(result, dict) else result.__dict__
    
    # Upload the result to Firestore
    logger.info(f"Uploading result to Firestore: {result_dict}")
    try:
        doc_id = firebase_service.upload_to_firestore(result_dict)
        logger.info(f"Document ID: {doc_id}")
    except Exception as e:
        logger.error(f"Failed to upload to Firestore: {e}")

if __name__ == "__main__":
    main()
