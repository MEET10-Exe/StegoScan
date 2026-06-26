from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(user, history):

    os.makedirs("static", exist_ok=True)
    file_path = os.path.join("static", f"{user}_report.pdf")

    c = canvas.Canvas(file_path, pagesize=letter)

    c.drawString(50, 750, "🛡 STEGOSCAN REPORT")
    c.drawString(50, 730, f"USER: {user}")

    y = 700

    if not history:
        c.drawString(50, y, "No scan history available")
    else:
        for h in history[-20:]:
            text = f"{h.get('time','')} | {h.get('file','')} | {h.get('status','')} | {h.get('score','')}"
            c.drawString(50, y, text)
            y -= 20

            if y < 50:
                c.showPage()
                y = 750

    c.save()
    return file_path