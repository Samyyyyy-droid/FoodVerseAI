
import cv2
import numpy as np


def preprocess_hygiene_frame(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image")

    height, width, channels = image.shape

    resized = cv2.resize(image, (640, 480))

    gray = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2GRAY
    )

    hsv = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2HSV
    )

    brightness = float(np.mean(gray))
    saturation = float(np.mean(hsv[:, :, 1]))

    edges = cv2.Canny(gray, 100, 200)

    edge_density = float(np.mean(edges > 0))

    return {
        "original_width": width,
        "original_height": height,
        "channels": channels,
        "processed_width": 640,
        "processed_height": 480,
        "brightness": round(brightness, 2),
        "saturation": round(saturation, 2),
        "edge_density": round(edge_density, 4)
    }
