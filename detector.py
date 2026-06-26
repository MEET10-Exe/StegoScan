from PIL import Image
import numpy as np

def analyze_image(path):
    try:
        img = Image.open(path)
        img_rgb = img.convert("RGB")

        arr = np.array(img_rgb)

        width, height = img.size
        image_format = img.format if img.format else "Unknown"

        risk = float(np.std(arr)) / 128 * 100
        risk = min(risk, 100)

        if risk > 60:
            status = "HIGH RISK"
        elif risk > 30:
            status = "MEDIUM RISK"
        else:
            status = "LOW RISK"

        return {
            "status": status,
            "percentage": round(risk, 2),
            "security_score": round(100 - risk, 2),
            "width": width,
            "height": height,
            "format": image_format
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "percentage": 0,
            "security_score": 0,
            "width": 0,
            "height": 0,
            "format": "Unknown"
        }