import os
import requests
import google.generativeai as genai
import googleapiclient.discovery
from moviepy.editor import VideoFileClip, concatenate_videoclips

# ==========================================
# ১. এপিআই কি ও ক্রেডেনশিয়াল কনফিগারেশন
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6Ifj-dLl-pwvmiQLqMNr_ByGoB46T-T59OElRR7bznEyw"
genai.configure(api_key=GEMINI_API_KEY)

# ইউটিউব কনফিগারেশন
YOUTUBE_API_KEY = "AIzaSyCYCCDisaaxkvH6J58G-pN4QurCi__Cw_w"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# মেটা (Facebook / Instagram / Threads) কনফিগারেশন
META_ACCESS_TOKEN = "14faf3eddb9f165c97456d9d82fbe29b"
FACEBOOK_PAGE_ID = "YOUR_PAGE_ID"          # আপনার ফেসবুক পেজ আইডি
INSTAGRAM_ACCOUNT_ID = "YOUR_IG_ID"        # আপনার ইনস্টাগ্রাম অ্যাকাউন্ট আইডি
THREADS_USER_ID = "YOUR_THREADS_USER_ID"   # আপনার থ্রেডস ইউজার আইডি

# ==========================================
# ২. মাস্টার প্রম্পট কনফিগারেশন
# ==========================================
MASTER_STYLE_PROMPT = """
Role: High-end animation director & scriptwriter.
Visual Style: 2D Cartoon animation, vibrant lighting, clean vector outlines, 
consistent character design, dynamic camera movement, optimized for 9:16 vertical shorts.
Script Tone: Engaging, fast-paced storytelling, punchy hook in the first 3 seconds.
"""

# ==========================================
# ৩. জেমিনি দিয়ে কন্টেন্ট ও ইমেজ/ভিডিও প্রম্পট জেনারেট
# ==========================================
def generate_pipeline_content(topic):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    {MASTER_STYLE_PROMPT}

    Topic: {topic}

    Please provide the output strictly in this structure:
    ---SCRIPT---
    (A short 30-45 second narration script)
    ---METADATA---
    Title: (Catchy YouTube & Reels title)
    Description: (SEO-friendly description with hashtags)
    ---SCENES---
    1. Visual scene description matching the cartoon style.
    2. Visual scene description matching the cartoon style.
    3. Visual scene description matching the cartoon style.
    """
    
    response = model.generate_content(prompt)
    return response.text

# ==========================================
# ৪. MoviePy দিয়ে একাধিক ক্লিপ জোড়া লাগানো
# ==========================================
def merge_generated_clips(clip_paths, final_output="output_video.mp4"):
    try:
        clips = [VideoFileClip(path) for path in clip_paths]
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(final_output, fps=24)
        print(f"[Success] Video created: {final_output}")
        return final_output
    except Exception as e:
        print(f"[Error] Failed to merge clips: {e}")
        return None

# ==========================================
# ৫. ইউটিউব ও মেটা এপিআই ইন্টিগ্রেশন হ্যান্ডলার
# ==========================================
def get_youtube_service():
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=YOUTUBE_API_KEY
    )

def post_to_meta_platforms(caption, video_url):
    payload = {
        "access_token": META_ACCESS_TOKEN,
        "caption": caption
    }
    print("[Meta API] Ready to trigger upload endpoints.")

# ==========================================
# ৬. অটোমেশন এক্সিকিউটর
# ==========================================
def run_automation_workflow(topic_name):
    print(f"\n[Running Workflow] Topic: {topic_name}")
    
    # স্ক্রিপ্ট, মেটাডাটা ও সিন তৈরি
    ai_data = generate_pipeline_content(topic_name)
    print("\n--- AI Production Plan ---")
    print(ai_data)

if __name__ == "__main__":
    print("AI Video Automation Engine initialized.")
    
    sample_topic = "রহস্যময় মহাকাশের অজানা তথ্য"
    run_automation_workflow(sample_topic)
