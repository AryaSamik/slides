def summarize_text(segments, num_slides):
    num_segments = len(segments)
    chunk_size = num_segments // num_slides
    summaries = []

    for i in range(num_slides):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < num_slides - 1 else num_segments
        chunk = segments[start_idx:end_idx]

        chunk_text = " ".join(seg["text"] for seg in chunk)
        timestamp = chunk[0]["start"]  # REAL timestamp in seconds

        summaries.append({
            "text": chunk_text,
            "timestamp": timestamp
        })

    return summaries