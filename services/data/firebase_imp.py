import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from services.data.firebase_service import FirebaseService

class FirebaseImp(FirebaseService):
    def __init__(self, firebase_cred_path, storage_bucket):
        self.firebase_cred_path = firebase_cred_path
        self.storage_bucket = storage_bucket
        self._initialize_app()
        self.db = firestore.client()

    def _initialize_app(self):
        cred = credentials.Certificate(self.firebase_cred_path)
        firebase_admin.initialize_app(cred, {'storageBucket': self.storage_bucket})
        self.storage_client = storage.bucket()

    def download_video_from_storage(self, video_name):
        blob = self.storage_client.blob(video_name)
        video_path = f"{video_name}"
        blob.download_to_filename(video_path)
        return video_path

    def upload_to_firestore(self, data):
        doc_ref = self.db.collection('AnalysisVideo').document()
        doc_ref.set(data)
        return doc_ref.id
