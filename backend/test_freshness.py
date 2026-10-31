
from services.freshness_ai import preprocess_food_image

IMAGE_PATH = "test_food.jpg"

try:
    result = preprocess_food_image(IMAGE_PATH)

    print("Image preprocessing successful!")
    print("\nExtracted Features:")

    for key, value in result["features"].items():
        print(f"{key}: {value}")

    print("\nImage encoding successful!")

except Exception as error:
    print("Error:", error)
