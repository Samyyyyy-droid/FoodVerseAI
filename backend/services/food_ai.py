
import os
import json
import base64
import mimetypes

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "qwen/qwen3.8-27b"


def analyze_food_image(image_path: str):

    if not client.api_key:
        raise ValueError("Groq API key is missing")

    mime_type, _ = mimetypes.guess_type(image_path)

    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Unsupported image format")

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    prompt = """
    You are a professional AI nutritionist and food scientist.

    Analyze the uploaded food image and estimate its nutritional
    composition using typical recipes and serving sizes.

    TASKS:

    1. Identify the food or drink.
    2. Estimate a reasonable serving size in grams.
    3. Estimate calories in kcal.
    4. Estimate protein in grams.
    5. Estimate carbohydrates in grams.
    6. Estimate fats in grams.
    7. Estimate fiber in grams.
    8. Estimate sugar in grams.
    9. Calculate a health score between 0 and 100.
    10. Assign a health label.
    11. Explain the nutritional assessment.
    12. Suggest two healthier alternatives.

    IMPORTANT:
    - Nutritional values must be estimates, not laboratory measurements.
    - Base estimates on a typical serving of the identified dish.
    - Do not invent ingredients that cannot reasonably be inferred.
    - Consider protein, fiber, sugar, fat and calories when
      evaluating nutritional quality.
    - Do not automatically classify every high-calorie food
      as unhealthy.
    - If the image does not contain food or a drink,
      return exactly {"error": "NOT_FOOD"}.

    HEALTH LABEL RULES:
    80-100: Healthy
    50-79: Moderate
    0-49: Unhealthy

    RETURN ONLY VALID JSON:

    {
        "dish_name": "Food name",
        "food_category": "Category",
        "serving_size": "250 g",
        "calories": 350,
        "protein": 15.5,
        "carbs": 28.0,
        "fats": 18.0,
        "fiber": 4.0,
        "sugar": 5.0,
        "health_score": 65,
        "health_label": "Moderate",
        "reasoning": "Nutritional assessment",
        "alternatives": [
            "Healthier alternative 1",
            "Healthier alternative 2"
        ],
        "nutrition_note": "Values are approximate estimates."
    }
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        max_completion_tokens=1200
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Empty response from AI model")

    result = result.replace("```json", "").replace("```", "").strip()

    data = json.loads(result)

    if data.get("error") == "NOT_FOOD":
        return data

    required_fields = [
        "dish_name",
        "food_category",
        "serving_size",
        "calories",
        "protein",
        "carbs",
        "fats",
        "fiber",
        "sugar",
        "health_score",
        "health_label",
        "reasoning",
        "alternatives"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing AI response field: {field}")

    return data
