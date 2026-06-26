from PIL import Image
import numpy as np

def analyze_image(image_path):

    try:
        image = Image.open(image_path).convert("RGB")
        arr = np.array(image)

        std = np.std(arr)
        risk = (std / 128) * 100

        if risk > 60:
            status = "HIGH RISK"
        elif risk > 30:
            status = "MEDIUM RISK"
        else:
            status = "LOW RISK"

        return {
            "status": status,
            "percentage": round(risk, 2),
            "security_score": round(100 - risk, 2)
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "percentage": 0,
            "security_score": 0
        }