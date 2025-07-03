import subprocess

def download_video_from_youtube(url, video_id):
    output_path = f"temp/{video_id}.mp4"
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(command, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return None
