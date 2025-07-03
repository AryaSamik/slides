from fastapi import FastAPI, Form
from download_video import download_video_from_youtube
from transcribe import transcribe_video
from summarize import summarize_text
from extract_frames import extract_key_frames
from generate_pdf import generate_slide_pdf

import uuid

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Slide Generator API!"}

try:
    @app.post("/generate")
    async def generate_slides(
        youtube_url: str = Form(...),
        num_slides: int = Form(5)  # default is 5 slides
    ):
        video_id = str(uuid.uuid4())
        
        video_path = download_video_from_youtube(youtube_url, video_id)
        if not video_path:
            return {"error": "Failed to download video. Please check the URL."}
        transcript = transcribe_video(video_path)
        # print(f"Transcript: {transcript}")
        summaries = summarize_text(transcript, num_slides)
        # print(f"Summaries: {summaries}")
        image_paths = extract_key_frames(video_path, summaries)
        pdf_path = generate_slide_pdf(summaries, image_paths, video_id)

        return {"pdf_url": f"/output/{pdf_path}"}
except Exception as e:
    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        return {"error": "some error occurred"}