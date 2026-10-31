from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.recipe_ai import generate_recipe

router = APIRouter(
    prefix="/api/kitchen",
    tags=["Smart Kitchen"]
)

class RecipeRequest(BaseModel):
    text_input: str
    image_description: str = ""

@router.post("/recipe")
async def create_recipe(request: RecipeRequest):
    try:
        result = generate_recipe(
            text_input=request.text_input,
            image_description=request.image_description
        )
        return {
            "success": True,
            "message": "Recipe generated successfully",
            "data": result
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))