
import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from services.food_ai import analyze_food_image

router = APIRouter(
    prefix="/api/food-recognition",
    tags=["Food Recognition"]
)

UPLOAD_DIR = "temp_uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed"
        )

    image_path = os.path.join(
        UPLOAD_DIR,
        f"{uuid.uuid4().hex}_{os.path.basename(file.filename or 'image')}"
    )

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty"
            )

        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Image size must not exceed 10 MB"
            )

        with open(image_path, "wb") as image:
            image.write(contents)

        result = analyze_food_image(image_path)

        if result.get("error") == "NOT_FOOD":
            raise HTTPException(
                status_code=400,
                detail="The uploaded image does not contain food"
            )

        return {
            "success": True,
            "message": "Food identified successfully",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
