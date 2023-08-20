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


# searches Youtube based on query parameter
# returns: list of dicts (one per search result), each dict contains title of video and video_id for one video
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


#  gets description of video provided by video_id
#  returns: string (video description)
def yt_get_video_description(youtube, video_id):
    video_response = youtube.videos().list(part="snippet", id=video_id).execute()

    if video_response.get("items"):
        video_info = video_response["items"][0]["snippet"]
        return video_info.get("description", "Description not available")
    else:
        return "Video not found."


# creates a playlist and returns its id
def yt_create_playlist(youtube, title, description):
    playlist_body = {
        "snippet": {
            "title": title,
            "description": description,
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "private"  # You can change this to "public" if desired
        },
    }

    playlist_response = (
        youtube.playlists().insert(part="snippet,status", body=playlist_body).execute()
    )
    return playlist_response["id"]


# takes in playlist id and list of video ids and inserts the videos into the playlist
def yt_add_videos_to_playlist(youtube, playlist_id, video_ids):
    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": 0,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        )
        request.execute()
        print(f"Video {video_id} added to playlist.")
