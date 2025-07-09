import { useState } from "react";
import axios from "axios";

function Generator() {
  const [youtubeURL, setYoutubeURL] = useState("");
  const [numSlides, setNumSlides] = useState(5);
  const [pdfUrl, setPdfUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPdfUrl("");

    const formData = new FormData();
    formData.append("youtube_url", youtubeURL);
    formData.append("num_slides", numSlides);

    try {
      const response = await axios.post(
        "http://localhost:8000/generate",
        formData
      );
      const { pdf_url } = response.data;
      setPdfUrl(`http://localhost:8000${pdf_url}`);
    } catch (error) {
      console.error("Error generating slides:", error);
      alert("Failed to generate PDF. Check your URL or backend.");
    }

    setLoading(false);
  };

  return (
    <>
      <div>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={youtubeURL}
            onChange={(e) => setYoutubeURL(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Number of slides"
            value={numSlides}
            onChange={(e) => setNumSlides(e.target.value)}
            min="1"
            max="20"
          />
          <button type="submit">Generate Slides</button>
        </form>

        {loading && <p>Processing... Please wait</p>}
        {pdfUrl && (
          <div>
            <p>PDF Ready:</p>
            <a href={pdfUrl} target="" rel="noopener noreferrer" download>
              Download PDF
            </a>
          </div>
        )}
      </div>
    </>
  );
}

export default Generator;