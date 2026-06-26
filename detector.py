from PIL import Image
import numpy as np

def analyze_image(path):
    try:
        img = Image.open(path).convert("RGB")
        arr = np.array(img)

        risk = float(np.std(arr)) / 128 * 100

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

    except:
        return {
            "status": "ERROR SAFE MODE",
            "percentage": 0,
            "security_score": 0
        }