import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "qwen/qwen3.8-27b"


def generate_meal_plan(user_profile: dict):

    if not client.api_key:
        raise ValueError("Groq API key is missing")

    prompt = f"""
    Create a personalized one-day meal plan using this user profile:

    {json.dumps(user_profile)}

    Return ONLY valid JSON with this exact structure:

    {{
        "daily_calorie_target": 2200,
        "total_estimated_calories": 2150,
        "diet_type": "Vegetarian",
        "goal": "Muscle gain",
        "meals": [
            {{
                "meal_name": "Breakfast",
                "time": "8:00 AM",
                "food_items": [
                    {{
                        "name": "Oats",
                        "quantity": "50g",
                        "calories": 190
                    }}
                ],
                "total_calories": 350,
                "description": "High protein breakfast"
            }}
        ],
        "nutrition_summary": {{
            "protein": "100g",
            "carbohydrates": "250g",
            "fats": "65g",
            "fiber": "30g"
        }},
        "recommendations": [
            "Drink sufficient water throughout the day"
        ]
    }}

    IMPORTANT:
    - Generate exactly the number of meals requested.
    - Respect dietary preferences and allergies.
    - Use foods appropriate to the user's location and preferences.
    - Keep total calories reasonably close to the target.
    - Return valid JSON only. No markdown or explanations outside JSON.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a professional nutrition and meal planning assistant. Always return valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Empty response received from AI")

    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON response from AI: {error}")
        raise ValueError(f"Invalid JSON response from AI: {error}")