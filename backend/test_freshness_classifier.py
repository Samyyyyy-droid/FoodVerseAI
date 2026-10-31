
from services.freshness_ai import preprocess_food_image
from services.freshness_classifier import classify_freshness

IMAGE_PATH = "test_food.jpg"

try:
    # Preprocess food image
    processed = preprocess_food_image(IMAGE_PATH)

    # Classify food freshness
    result = classify_freshness(
        processed["features"],
        food_name="Paneer Butter Masala"
    )

    print("\nFRESHNESS ANALYSIS RESULT")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nFreshness classification test completed!")

except Exception as error:
    print("Error:", error)
