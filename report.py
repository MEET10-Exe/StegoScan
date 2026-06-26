from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_pdf(user,history):

    os.makedirs(
        "static",
        exist_ok=True
    )

    file_path=f"static/{user}_report.pdf"

    c=canvas.Canvas(
        file_path,
        pagesize=letter
    )

    c.drawString(
        50,
        780,
        "STEGOSCAN REPORT"
    )

    c.drawString(
        50,
        760,
        f"User: {user}"
    )

    y=720

    if not history:

        c.drawString(
            50,
            y,
            "No scan history"
        )

    else:

        for h in history:

            text=f"""
{h['time']}
{h['file']}
{h['status']}
Score:{h['score']}
"""

            c.drawString(
                50,
                y,
                text[:80]
            )

            y-=30

            if y<50:

                c.showPage()
                y=780

    c.save()

    return file_path