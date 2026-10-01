from googleapiclient.discovery import build
import webbrowser
from neura_engine.config import YOUTUBE_API_KEY
from neura_engine.command import speak

def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", type="video", maxResults=1)
    response = request.execute()

    if "items" in response and response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        title = response["items"][0]["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        speak(f"Playing {title} on YouTube.")
        webbrowser.open(url)
    else:
        speak("Sorry, no results found on YouTube.")