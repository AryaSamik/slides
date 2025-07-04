import yt_dlp
import re

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hrs > 0:
        return f"{hrs:02}:{mins:02}:{secs:02}"
    else:
        return f"{mins:02}:{secs:02}"


def get_video_title(video_url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('title', 'Untitled Video')
    except Exception as e:
        print("yt_dlp failed:", e)
        return "Untitled Video"

def get_youtube_thumbnail(video_url):
    # Extract video ID from URL
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
    if not match:
        return None
    video_id = match.group(1)
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"