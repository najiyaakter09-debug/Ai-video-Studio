import os
import requests
import googleapiclient.discovery

# ১. ইউটিউব এপিআই কনফিগারেশন
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


# ২. মেটা (ফেসবুক, ইনস্টাগ্রাম ও থ্রেডস) কনফিগারেশন
ACCESS_TOKEN = "14faf3eddb9f165c97456d9d82fbe29b"
FACEBOOK_PAGE_ID = ""
INSTAGRAM_USER_ID = ""
THREADS_USER_ID = ""

# ফেসবুক পোস্ট ফাংশন
def post_to_facebook(message):
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

# ইনস্টাগ্রাম পোস্ট ফাংশন
def post_to_instagram(image_url, caption):
    container_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media"
    container_payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(container_url, data=container_payload)
    result = response.json()
    
    if 'id' in result:
        creation_id = result['id']
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        return publish_response.json()
    
    return result

# থ্রেডস পোস্ট ফাংশন
def post_to_threads(image_url, caption):
    container_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    container_payload = {
        'media_type': 'IMAGE',
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(container_url, data=container_payload)
    result = response.json()
    
    if 'id' in result:
        creation_id = result['id']
        publish_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        return publish_response.json()
    
    return result


if __name__ == "__main__":
    print("AI Video Studio Backend is ready for YouTube, Facebook, Instagram, and Threads!")
