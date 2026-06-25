from reportlab.pdfgen import canvas

def create_pdf(result):

    filename = "report.pdf"

    c = canvas.Canvas(filename)

    c.drawString(100, 800, "StegoScan Report")
    c.drawString(100, 770, f"Status: {result['status']}")
    c.drawString(100, 740, f"LSB Percentage: {result['percentage']}%")

    c.save()

    return filename