
import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.hygiene_ai import preprocess_hygiene_frame
from services.hygiene_classifier import analyze_hygiene

router = APIRouter(
    prefix="/api/hygiene",
    tags=["Restaurant Hygiene Monitoring"]
)


@router.post("/analyze")
async def analyze_kitchen(
    file: UploadFile = File(...),
    context: str = Form("Restaurant kitchen inspection")
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

        features = preprocess_hygiene_frame(temp_path)

        result = analyze_hygiene(
            temp_path,
            context=context
        )

        return {
            "success": True,
            "message": "Hygiene analysis completed",
            "image_features": features,
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
