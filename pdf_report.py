from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(image_path, disease, confidence, treatment,
                 symptoms, prevention, output_path):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Plant Disease Detection Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    if os.path.exists(image_path):
        img = Image(image_path, width=250, height=250)
        story.append(img)
        story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Disease:</b> {disease}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Confidence:</b> {confidence:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Treatment:</b> {treatment}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Symptoms:</b> {symptoms}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Prevention:</b> {prevention}", styles["BodyText"]))

    doc.build(story)