from fpdf import FPDF
import os

def generate_slide_pdf(summaries, images, video_id):
    pdf = FPDF()
    for i, point in enumerate(summaries):
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=f"Slide {i+1}: {point['text']}", ln=True)
        pdf.image(images[i], x=10, y=30, w=180)

    output_path = f"output/{video_id}.pdf"
    pdf.output(output_path)
    return f"{video_id}.pdf"
