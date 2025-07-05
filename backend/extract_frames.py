from moviepy import VideoFileClip
import os

def extract_key_frames(video_path, summaries, video_id):
    clip = VideoFileClip(video_path)
    image_paths = []

    for i, point in enumerate(summaries):
        path = f"temp/{video_id}/frame_{i}.jpg"
        clip.save_frame(path, t=point['timestamp'])
        image_paths.append(path)
    
    clip.close()

    return image_paths
