# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
import random
import json


#initialize_app()

@https_fn.on_request()
def demo_function(req: https_fn.Request) -> https_fn.Response:
    word = "Python"
    number = random.randint(1, 100)  # Generate a random number between 1 and 100
    response_data = {
        "word": word,
        "number": number
    }
    response_content = json.dumps(response_data)  # Convert the dictionary to a JSON string
    return response_content
