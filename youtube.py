import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

load_dotenv()

# set up credentials
YT_API_KEY = os.getenv("OPENAI_API_KEY")
CLIENT_SECRET_FILE = "auth/client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


# authenticate
def yt_authenticate():
    creds = None
    if CLIENT_SECRET_FILE:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=5566)  # 5566 or 8080
    elif YT_API_KEY:
        return build("youtube", "v3", developerKey=YT_API_KEY)
    return build("youtube", "v3", credentials=creds)


def yt_search(youtube, query, max_results=10):
    search_response = (
        youtube.search()
        .list(q=query, part="id,snippet", maxResults=max_results)
        .execute()
    )

    search_results = []

    for item in search_response.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            search_results.append({"title": title, "video_id": video_id})

    return search_results


def yt_get_caption_track(youtube, video_id):
    captions_response = (
        youtube.captions().list(part="snippet", videoId=video_id).execute()
    )

    captions = []

    for item in captions_response.get("items", []):
        caption_id = item["id"]
        caption_language = item["snippet"]["language"]
        captions.append({"id": caption_id, "language": caption_language})

    return captions


def yt_download_caption(youtube, track_id):
    caption_response = (
        youtube.captions()
        .download(
            id=track_id,
            tfmt="srt",  # You can change the format to "ttml" for other formats
        )
        .execute()
    )

    caption_url = caption_response["downloadUrl"]
    caption_text = requests.get(caption_url).text
    return caption_text


def yt_get_video_description(youtube, video_id):
    video_response = youtube.videos().list(part="snippet", id=video_id).execute()

    if video_response.get("items"):
        video_info = video_response["items"][0]["snippet"]
        return video_info.get("description", "Description not available")
    else:
        return "Video not found."
