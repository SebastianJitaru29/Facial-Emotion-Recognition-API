from services.emotion_analysis.emotion_analysis_imp import EmotionsAnalysisImp
from services.data.firebase_imp import FirebaseImp

def main():
    # Initialize the FirebaseService
    firebase_service = FirebaseImp(firebase_cred_path="firebase/backend-testing-tfg-firebase-adminsdk-vx45t-d0c10e29bd.json", storage_bucket="gs://backend-testing-tfg.appspot.com")

    # Perform emotion analysis on the video
    emotion_analysis_service = EmotionsAnalysisImp(model_path="models/model2/model2.h5")
    video_path = "static/videos/my_face_video1.mp4"  # Path to the video you want to analyze
    result = emotion_analysis_service.get_emotion_percentages(video_path)
    
    print("The result is:", result)
    
    # Convert the result to a dictionary (if it isn't already)
    result_dict = result if isinstance(result, dict) else result.__dict__
    print("The result in dictionary format is:", result_dict)
    
    # Download last video updated to firebase storage
    #video_path = firebase_service.download_video_from_storage("my_face_video.mp4")


    # Upload the result to Firestore
    doc_id = firebase_service.upload_to_firestore(result_dict)
    print("Document ID:", doc_id)


if __name__ == "__main__":
    main()
