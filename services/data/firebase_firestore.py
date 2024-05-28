from firebase_admin import credentials, firestore, initialize_app
from google.cloud import storage

class FirebaseService:
    def __init__(self, firebase_cred_path):
        self.firebase_cred_path = firebase_cred_path
        self.storage_client = None
    
    def initialize_app(self):
        cred = credentials.Certificate(self.firebase_cred_path)
        initialize_app(cred, {'storageBucket': '<myBucket>'})
        self.storage_client = storage.Client()

    def download_video_from_storage(self, video_name):
        # Implement video download logic here
        print(video_name)
        return "static/videos/my_face_video.mp4"
        pass

    def upload_to_firestore(self, data):
        # Implement Firestore upload logic here
        print(data)
        pass
