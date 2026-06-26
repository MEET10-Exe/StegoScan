from PIL import Image
import numpy as np
import os

def analyze_image(image_path: str) -> dict:
    """
    Analyze an image for potential hidden data risk.
    
    Parameters:
        image_path (str): Path to the image file.
    
    Returns:
        dict: Analysis results including risk level, score, dimensions, and format.
    """
    try:
        # --- Load image safely ---
        image = Image.open(image_path).convert("RGB")
        img_array = np.array(image)

        width, height = image.size

        # --- Basic pixel statistics ---
        mean_pixel = float(np.mean(img_array))
        std_pixel = float(np.std(img_array))

        # --- Risk calculation ---
        risk = (std_pixel / 128) * 100
        risk = max(0, min(risk, 100))  # clamp between 0–100

        if risk > 60:
            status = "HIGH RISK"
        elif risk > 30:
            status = "MEDIUM RISK"
        else:
            status = "LOW RISK"

        # --- File size in KB ---
        file_size_kb = round(os.path.getsize(image_path) / 1024, 2)

        return {
            "status": status,
            "percentage": round(risk, 2),
            "security_score": round(100 - risk, 2),
            "width": width,
            "height": height,
            "format": image.format or "unknown",
            "mean_pixel": round(mean_pixel, 2),
            "std_pixel": round(std_pixel, 2),
            "file_size_kb": file_size_kb
        }

    except Exception as e:
        # --- Fallback in case of error ---
        return {
            "status": "ERROR",
            "message": str(e),
            "percentage": 0,
            "security_score": 0,
            "width": 0,
            "height": 0,
            "format": "unknown",
            "mean_pixel": 0,
            "std_pixel": 0,
            "file_size_kb": 0
        }
