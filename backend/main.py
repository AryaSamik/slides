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
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from db import users_collection
from auth import hash_password, verify_password, create_access_token, decode_access_token
from models import UserIn
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
from auth import token_blacklist

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
    thumbnail_url = get_youtube_thumbnail(youtube_url)
    video_title = get_video_title(youtube_url)

    # Download thumbnail image
    if thumbnail_url:
        thumbnail_path = f"temp/{video_id}/thumbnail.jpg"
    try:
        with open(thumbnail_path, 'wb') as f:
            f.write(requests.get(thumbnail_url).content)
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
        thumbnail_path = None

    video_path = download_video_from_youtube(youtube_url, video_id)
    if not video_path:
        return {"error": "Failed to download video. Please check the URL."}
    transcript_data = transcribe_video(video_path)
    segments = transcript_data["segments"]
    duration = transcript_data["duration"]
    summaries = summarize_text(segments, num_slides, duration)
    image_paths = extract_key_frames(video_path, summaries, video_id)
    pdf_path = generate_slide_pdf(summaries, image_paths, video_id, youtube_url, video_title, thumbnail_path)

    time.sleep(1)  # short pause before deleting

    #Clean up temporary files
    cleanup_temp_files(f"temp/{video_id}")

    return {
        "pdf_url": f"/output/{pdf_path}",
        "download_link": f"http://localhost:8000/output/{pdf_path}"
    }

@app.post("/signup")
async def signup(user: UserIn):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    result = await users_collection.insert_one({"email": user.email, "password": hashed_pw})
    # print(result)
    return {"message": "User created"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    # Optionally decode and verify token here
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Blacklist the token
    token_blacklist.add(token)
    return {"message": "Logout successful"}