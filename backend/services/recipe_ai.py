
import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "qwen/qwen3.8-27b"


def generate_recipe(text_input="", image_description=""):

    prompt = f"""
    You are a professional chef and cooking assistant.

    Generate a detailed cooking recipe using the following input.

    User input: {text_input}
    Food image description: {image_description}

    Return valid JSON in this format:

    {{
        "dish_name": "Dish name",
        "description": "Short description",
        "ingredients": [
            {{
                "name": "Ingredient",
                "quantity": "Amount"
            }}
        ],
        "preparation_time": "Minutes",
        "cooking_time": "Minutes",
        "difficulty": "Easy, Medium or Hard",
        "servings": 2,
        "steps": [
            {{
                "step": 1,
                "instruction": "Cooking instruction",
                "duration": "Minutes"
            }}
        ],
        "cooking_tips": [],
        "nutritional_note": "Approximate nutritional information"
    }}

    Provide practical cooking instructions.
    Return JSON only.
    """

    if not text_input.strip() and not image_description.strip():
        raise ValueError("Please provide cooking input")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        response_format={"type": "json_object"}
    )

    return json.loads(
        response.choices[0].message.content
    )
