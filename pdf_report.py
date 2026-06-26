from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(result):

    filename = "StegoScan_Report.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 800, "StegoScan Report")

    c.setFont("Helvetica", 12)

    c.drawString(50, 760, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    c.drawString(50, 730, f"Risk Status : {result['status']}")
    c.drawString(50, 705, f"Risk Percentage : {result['percentage']} %")
    c.drawString(50, 680, f"Security Score : {result['security_score']} %")
    c.drawString(50, 655, f"Resolution : {result['width']} x {result['height']}")
    c.drawString(50, 630, f"Image Format : {result['format']}")

    c.line(50, 615, 550, 615)

    c.drawString(50, 590, "Recommendation:")

    if result["status"] == "HIGH RISK":
        c.drawString(70, 565, "Possible hidden data detected. Further investigation recommended.")
    elif result["status"] == "MEDIUM RISK":
        c.drawString(70, 565, "Image appears suspicious. Manual verification suggested.")
    else:
        c.drawString(70, 565, "No significant hidden data indicators found.")

    c.save()

    return filename