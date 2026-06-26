from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(user, history):
    file_path = f"{user}_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(50, 750, f"StegoScan Report - User: {user}")

    y = 700

    for h in history[-15:]:
        line = f"{h.get('time','')} | {h.get('file','')} | {h.get('status','')} | Score: {h.get('score','')}"
        c.drawString(50, y, line)
        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return file_path