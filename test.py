import os
import zipfile
import requests

def download_and_extract_zip(url, extract_to='.'):
    local_filename = url.split('/')[-1]
    # Download the file from `url` and save it locally under `local_filename`:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    # Extract the downloaded file
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(local_filename)  # Remove the zip file after extraction

# Example URL for Actor_01 Video Speech
url = "https://zenodo.org/record/1188976/files/Video_Speech_Actor_01.zip?download=1"
download_and_extract_zip(url, extract_to='.')

# Repeat the above two lines for other actors
