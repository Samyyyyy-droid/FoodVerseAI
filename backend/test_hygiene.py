
from services.hygiene_ai import preprocess_hygiene_frame
from services.hygiene_classifier import analyze_hygiene

IMAGE_PATH = "test_kitchen.jpg"

try:
    # Extract image features
    features = preprocess_hygiene_frame(IMAGE_PATH)

    print("\nIMAGE PREPROCESSING")
    print("-" * 40)

    for key, value in features.items():
        print(f"{key}: {value}")

    # Perform AI hygiene analysis
    result = analyze_hygiene(
        IMAGE_PATH,
        context="Restaurant kitchen inspection"
    )

    print("\nHYGIENE ANALYSIS RESULT")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nHygiene analysis completed!")

except Exception as error:
    print("Error:", error)
