
import os
import json
import base64

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "qwen/qwen3.8-27b"


def analyze_hygiene(image_path, context="Restaurant kitchen inspection"):

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    prompt = f"""
    You are a professional restaurant hygiene inspector.

    Analyze this kitchen image.

    Inspection context: {context}

    Check for:
    1. Food handlers wearing gloves.
    2. Proper hair protection.
    3. Clean food preparation surfaces.
    4. Visible waste or dirty floors.
    5. Safe food handling practices.

    Do not assume violations when evidence is unclear.
    Mark unobservable conditions as Unknown.

    Return valid JSON with this structure:

    {{
        "overall_score": 0,
        "compliance_level": "Good",
        "violations": [
            {{
                "violation": "Description",
                "severity": "High",
                "location": "Observed area",
                "reason": "Explanation"
            }}
        ],
        "observations": [],
        "recommendations": [],
        "ai_summary": "Inspection summary"
    }}

    Score must be between 0 and 100.
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
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    result = json.loads(
        response.choices[0].message.content
    )

    return result
