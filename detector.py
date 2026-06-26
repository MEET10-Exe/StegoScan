from PIL import Image
import numpy as np

def analyze_image(image_path):

    try:
        image = Image.open(image_path).convert("RGB")

        width, height = image.size
        img_array = np.array(image)

        lsb_count = 0
        total = img_array.size

        for value in img_array.flatten():
            if value & 1:
                lsb_count += 1

        percentage = (lsb_count / total) * 100

        if 48 <= percentage <= 52:
            status = "HIGH RISK"
        elif 45 <= percentage <= 55:
            status = "MEDIUM RISK"
        else:
            status = "LOW RISK"

        return {
            "status": status,
            "percentage": round(percentage, 2),
            "width": width,
            "height": height,
            "format": image.format or "unknown",
            "security_score": round(100 - percentage, 2)
        }

    except Exception:
        return {
            "status": "ERROR",
            "percentage": 0,
            "width": 0,
            "height": 0,
            "format": "unknown",
            "security_score": 0
        }