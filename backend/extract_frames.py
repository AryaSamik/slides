from moviepy import VideoFileClip
import os

def extract_key_frames(video_path, summaries):
    clip = VideoFileClip(video_path)
    image_paths = []

    for i, point in enumerate(summaries):
        frame = clip.get_frame(point['timestamp'])
        path = f"temp/frame_{i}.jpg"
        clip.save_frame(path, t=point['timestamp'])
        image_paths.append(path)

    return image_paths
