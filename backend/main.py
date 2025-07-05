from fastapi import FastAPI, Form
from download_video import download_video_from_youtube
from transcribe import transcribe_video
from summarize import summarize_text
from extract_frames import extract_key_frames
from generate_pdf import generate_slide_pdf
import os
import requests
from utils import get_youtube_thumbnail, get_video_title
from fastapi.staticfiles import StaticFiles
from utils import cleanup_temp_files
import uuid
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origin (adjust the port if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "*" for all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    if not os.path.exists(f"temp/{video_id}"):
        os.mkdir(f"temp/{video_id}")
    if not os.path.exists(f"output/{video_id}"):
        os.mkdir(f"output/{video_id}")
    start= time.time()
    thumbnail_url = get_youtube_thumbnail(youtube_url)
    print("Thumbnail URL fetch time: ", time.time() - start)
    start = time.time()
    video_title = get_video_title(youtube_url)
    print("Video title fetch time: ", time.time() - start)

    start = time.time()
    # Download thumbnail image
    if thumbnail_url:
        thumbnail_path = f"temp/{video_id}/thumbnail.jpg"
    try:
        with open(thumbnail_path, 'wb') as f:
            f.write(requests.get(thumbnail_url).content)
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
        thumbnail_path = None
    print("Thumbnail download time: ", time.time() - start)

    start = time.time()
    video_path = download_video_from_youtube(youtube_url, video_id)
    print("Video download time: ", time.time() - start)
    if not video_path:
        return {"error": "Failed to download video. Please check the URL."}
    start = time.time()
    transcript_data = transcribe_video(video_path)
    print("Transcription time: ", time.time() - start)
    segments = transcript_data["segments"]
    duration = transcript_data["duration"]
    start = time.time()
    summaries = summarize_text(segments, num_slides, duration)
    print("Summarization time: ", time.time() - start)
    start = time.time()
    image_paths = extract_key_frames(video_path, summaries, video_id)
    print("Frame extraction time: ", time.time() - start)
    start = time.time()
    pdf_path = generate_slide_pdf(summaries, image_paths, video_id, youtube_url, video_title, thumbnail_path)
    print("PDF generation time: ", time.time() - start)

    time.sleep(1)  # short pause before deleting

    #Clean up temporary files
    cleanup_temp_files(f"temp/{video_id}")

    return {
        "pdf_url": f"/output/{pdf_path}",
        "download_link": f"http://localhost:8000/output/{pdf_path}"
    }