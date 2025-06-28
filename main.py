import subprocess
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

def make_video():
    subprocess.call(['bash', 'ffmpeg.sh'])

def youtube_auth():
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=8080)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_to_youtube():
    from googleapiclient.http import MediaFileUpload

    youtube = youtube_auth()
    request_body = {
        'snippet': {
            'title': 'Lo-fi Mix Upload',
            'description': 'Generated automatically',
            'tags': ['lofi', 'music', '1 hour'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload('output.mp4', resumable=True)
    request = youtube.videos().insert(part='snippet,status', body=request_body, media_body=media)
    response = request.execute()
    print("✅ Uploaded: https://youtube.com/watch?v=" + response['id'])

# --- Run everything ---
if __name__ == '__main__':
    make_video()
    upload_to_youtube()
