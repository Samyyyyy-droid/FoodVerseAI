
import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.freshness_ai import preprocess_food_image
from services.freshness_classifier import classify_freshness

router = APIRouter(
    prefix="/api/freshness",
    tags=["Food Freshness Detection"]
)


@router.post("/analyze")
async def analyze_freshness(
    file: UploadFile = File(...),
    food_name: str = Form("Food")
):
    temp_path = None

    try:
        os.makedirs("temp_uploads", exist_ok=True)

        extension = os.path.splitext(file.filename)[1] or ".jpg"
        temp_path = os.path.join(
            "temp_uploads",
            f"{uuid.uuid4().hex}{extension}"
        )

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        processed = preprocess_food_image(temp_path)

        result = classify_freshness(
            processed["features"],
            food_name=food_name
        )

        return {
            "success": True,
            "message": "Freshness analysis completed",
            "data": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
