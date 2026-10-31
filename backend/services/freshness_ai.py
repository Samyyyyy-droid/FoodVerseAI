
import cv2
import numpy as np
import base64
import os

from PIL import Image
from io import BytesIO


def preprocess_food_image(image_path: str):

    if not os.path.exists(image_path):
        raise FileNotFoundError("Food image not found")

    # Load image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read the uploaded image")

    # Extract original dimensions
    height, width, channels = image.shape

    # Resize image for consistent processing
    resized = cv2.resize(
        image,
        (512, 512),
        interpolation=cv2.INTER_AREA
    )

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2RGB
    )

    # Convert image to HSV for colour analysis
    hsv_image = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2HSV
    )

    # Extract colour features
    mean_color = np.mean(rgb_image, axis=(0, 1))

    # Extract brightness
    brightness = float(np.mean(hsv_image[:, :, 2]))

    # Extract saturation
    saturation = float(np.mean(hsv_image[:, :, 1]))

    # Extract edge information using Canny
    edges = cv2.Canny(
        cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY),
        100,
        200
    )

    edge_density = float(np.mean(edges > 0))

    # Encode processed image as Base64
    pil_image = Image.fromarray(rgb_image)

    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG", quality=90)

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    # Prepare extracted features
    features = {
        "original_width": width,
        "original_height": height,
        "channels": channels,
        "processed_width": 512,
        "processed_height": 512,
        "mean_red": round(float(mean_color[0]), 2),
        "mean_green": round(float(mean_color[1]), 2),
        "mean_blue": round(float(mean_color[2]), 2),
        "brightness": round(brightness, 2),
        "saturation": round(saturation, 2),
        "edge_density": round(edge_density, 4)
    }

    return {
        "image_base64": image_base64,
        "features": features
    }
