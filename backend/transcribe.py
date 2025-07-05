import whisper
from moviepy import VideoFileClip

model = whisper.load_model("base")

def transcribe_video(video_path):
    result = model.transcribe(video_path)
    
    clip = VideoFileClip(video_path)
    duration = clip.duration  # duration in seconds
    clip.close()

    return {
        "segments": result['segments'], # har segment mein start, end, text
        "duration": duration
    }