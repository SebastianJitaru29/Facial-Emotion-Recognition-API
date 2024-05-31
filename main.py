from services.emotion_analysis.emotion_analysis_imp import EmotionsAnalysisImp

def main():
    emotion_analysis_service = EmotionsAnalysisImp(model_path="models/model2/model2.h5")
    video_path = "static/videos/my_face_video.mp4"  # Path to the video you want to analyze
    result = emotion_analysis_service.get_emotion_percentages(video_path)
    print(result)

if __name__ == "__main__":
    main()
