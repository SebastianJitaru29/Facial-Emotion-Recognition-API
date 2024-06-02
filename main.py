import logging
import coloredlogs
from services.emotion_analysis.emotion_analysis_imp import EmotionsAnalysisImp
from services.data.firebase_imp import FirebaseImp

def main():
    coloredlogs.install(level="INFO", fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    firebase_cred_path = "firebase/backend-testing-tfg-firebase-adminsdk-vx45t-d0c10e29bd.json"
    storage_bucket = "backend-testing-tfg.appspot.com"  

    logger.info(f"Initializing Firebase with credentials: {firebase_cred_path} and bucket: {storage_bucket}")
    firebase_service = FirebaseImp(firebase_cred_path=firebase_cred_path, storage_bucket=storage_bucket)

    # Perform emotion analysis on the video (currently commented out)
    emotion_analysis_service = EmotionsAnalysisImp(model_path="models/model2/model2.h5")
    video_path = "static/videos/my_face_video1.mp4"  # Path to the video you want to analyze
    result = emotion_analysis_service.get_emotion_percentages(video_path)
    # print("The result is:", result)
    # Convert the result to a dictionary (if it isn't already)
    result_dict = result if isinstance(result, dict) else result.__dict__
    # print("The result in dictionary format is:", result_dict)

    # Download last video updated to Firebase storage
    video_name = "FB.mp4"
    logger.info(f"Attempting to download video: {video_name} from storage.")
    try:
        video_path = firebase_service.download_video_from_storage(video_name)
        logger.info(f"Video downloaded successfully to: {video_path}")
    except Exception as e:
        logger.error(f"Failed to download video: {e}")
        print(f"Failed to download video: {e}")

    # Upload the result to Firestore (currently commented out)
    doc_id = firebase_service.upload_to_firestore(result_dict)
    print("Document ID:", doc_id)

if __name__ == "__main__":
    main()
