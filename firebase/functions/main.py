from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app
import requests
import json

# Initialize Firebase app
initialize_app()

# Hello World function
@https_fn.on_request(region="europe-west1")
def hello_world(req: https_fn.Request) -> https_fn.Response:
    response_data = {
        "word1": "hello1 from firebase function in  TFG-BACKEND-TESTING project!",
        "word2": "world"
    }
    return https_fn.Response(json.dumps(response_data), mimetype="application/json")



# Function to send POST request when a video is uploaded, works if the api is deployed on the internet
@storage_fn.on_object_finalized(bucket="backend-tfg-1d0d5.appspot.com",region="europe-west1")
def on_video_upload(event: storage_fn.CloudEvent[storage_fn.StorageObjectData]) -> None:
    
    video_name = event.data.name
    if video_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        url = "http://localhost:5000/process_video"
        payload = {
            "video_name": video_name
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"POST request to {url} with payload {payload} returned status code {response.status_code}")
