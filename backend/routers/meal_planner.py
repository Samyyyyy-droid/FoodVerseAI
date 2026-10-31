
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from services.meal_planner import generate_meal_plan

router = APIRouter(
    prefix="/api/meal-planner",
    tags=["Personalized Meal Planner"]
)


class UserProfile(BaseModel):
    age: int = Field(ge=1, le=120)
    diet_type: str
    goal: str
    activity_level: str
    daily_calorie_target: int = Field(ge=500, le=10000)
    allergies: List[str] = []
    food_preferences: List[str] = []
    meals_per_day: int = Field(default=4, ge=1, le=8)


@router.post("/generate")
async def create_meal_plan(profile: UserProfile):
    try:
        result = generate_meal_plan(profile.model_dump())

        return {
            "success": True,
            "message": "Meal plan generated successfully",
            "data": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
