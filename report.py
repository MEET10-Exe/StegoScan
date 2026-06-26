from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(user, history):

    folder = "reports"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"{user}_report.pdf")

    c = canvas.Canvas(file_path, pagesize=letter)

    c.drawString(50, 750, "STEGO SCAN REPORT")
    c.drawString(50, 730, f"USER: {user}")

    y = 700

    if history:
        for h in history[-15:]:
            text = f"{h.get('time','')} | {h.get('file','')} | {h.get('status','')} | {h.get('score','')}"
            c.drawString(50, y, text)
            y -= 20

            if y < 50:
                c.showPage()
                y = 750
    else:
        c.drawString(50, 700, "NO HISTORY FOUND")

    c.save()

    return file_path