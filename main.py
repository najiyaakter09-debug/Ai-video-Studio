import os
import googleapiclient.discovery

# আপনার গুগল ক্লাউড থেকে পাওয়া এপিআই কি এখানে বসিয়ে দিন
API_KEY = "AIzaSyCYCCDisaaxkvH6J58G-pN4QurCi__Cw_w"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_youtube_client():
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
    )

def check_channel_info(channel_handle):
    youtube = get_youtube_client()
    request = youtube.channels().list(
        part="snippet,statistics",
        forHandle=channel_handle
    )
    response = request.execute()
    return response

if __name__ == "__main__":
    print("AI Video Studio Backend is ready!")
