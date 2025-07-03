from fpdf import FPDF
from utils import format_timestamp

def generate_slide_pdf(summaries, images, video_id):
    pdf = FPDF()

    for i, point in enumerate(summaries):
        pdf.add_page()
        pdf.set_font("Arial", size=16)

        #Slide title
        pdf.cell(200, 10, txt=f"Slide {i+1}", ln=True)

        #Add timestamp
        timestamp_str = format_timestamp(point['timestamp'])
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Timestamp: {timestamp_str}", ln=True)

        #Slide text
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 10, txt=point['text'])

        #Image
        if i < len(images):
            pdf.image(images[i], x=10, y=60, w=180)

    output_path = f"output/{video_id}.pdf"
    pdf.output(output_path)
    return f"{video_id}.pdf"
