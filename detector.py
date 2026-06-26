from PIL import Image
import numpy as np

def analyze_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        img_array = np.array(image)

        width, height = image.size

        mean_pixel = np.mean(img_array)
        std_pixel = np.std(img_array)

        risk = (std_pixel / 128) * 100

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
            "format": image.format or "unknown"
        }

    except Exception:
        return {
            "status": "ERROR",
            "percentage": 0,
            "security_score": 0,
            "width": 0,
            "height": 0,
            "format": "unknown"
        }