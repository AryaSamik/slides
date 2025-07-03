def split_transcript(text, num_chunks):
    words = text.split()
    chunk_size = len(words) // num_chunks
    chunks = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_chunks - 1 else len(words)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

    return chunks

def summarize_text(transcript, num_slides):
    chunks = split_transcript(transcript, num_slides)
    summaries = []

    for i, chunk in enumerate(chunks):
        summary_text = f"Slide {i+1}: {chunk[:100]}..."  # Fake summary for now
        summaries.append({
            "text": summary_text,
            "timestamp": (i + 1) * 30  # fake timestamp: 30s per slide
        })

    return summaries