from utils import generate_summary

def summarize_text(segments, num_slides, total_duration):
    slide_duration = total_duration // num_slides
    summaries = []

    for i in range(num_slides):
        start_time = i * slide_duration
        end_time = (i + 1) * slide_duration

        chunk = [
            seg for seg in segments
            if seg["start"] >= start_time and seg["start"] < end_time
        ]

        if not chunk:
            continue  # skip empty slide

        chunk_text = " ".join(seg["text"] for seg in chunk)
        timestamp = chunk[0]["start"]

        try:
            summary = generate_summary(chunk_text)
        except Exception as e:
            summary = chunk_text[:200] + "..."  # fallback

        summaries.append({
            "text": summary,
            "timestamp": timestamp
        })

    return summaries