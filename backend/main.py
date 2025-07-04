from fastapi import FastAPI, Form
from download_video import download_video_from_youtube
from transcribe import transcribe_video
from summarize import summarize_text
from extract_frames import extract_key_frames
from generate_pdf import generate_slide_pdf
from pytube import YouTube
import requests
from utils import get_youtube_thumbnail, get_video_title
from fastapi.staticfiles import StaticFiles

import uuid

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Slide Generator API!"}

app.mount("/output", StaticFiles(directory="output"), name="output")

@app.post("/generate")
async def generate_slides(
    youtube_url: str = Form(...),
    num_slides: int = Form(5)  # default is 5 slides
):
    video_id = str(uuid.uuid4())
    thumbnail_url = get_youtube_thumbnail(youtube_url)
    video_title = get_video_title(youtube_url)

    # Download thumbnail image
    if thumbnail_url:
        thumbnail_path = f"output/{video_id}_thumb.jpg"
    try:
        with open(thumbnail_path, 'wb') as f:
            f.write(requests.get(thumbnail_url).content)
    except:
        thumbnail_path = None

    video_path = download_video_from_youtube(youtube_url, video_id)
    if not video_path:
        return {"error": "Failed to download video. Please check the URL."}
    transcript_data = transcribe_video(video_path)
    segments = transcript_data["segments"]
    duration = transcript_data["duration"]
    summaries = summarize_text(segments, num_slides, duration)
    image_paths = extract_key_frames(video_path, summaries)
    pdf_path = generate_slide_pdf(summaries, image_paths, video_id, youtube_url, video_title, thumbnail_path)

    return {
        "pdf_url": f"/output/{pdf_path}",
        "download_link": f"http://localhost:8000/output/{pdf_path}"
    }