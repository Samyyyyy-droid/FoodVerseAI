
from services.meal_planner import generate_meal_plan

user_profile = {
    "age": 21,
    "diet_type": "Vegetarian",
    "goal": "Muscle gain",
    "activity_level": "Moderately active",
    "daily_calorie_target": 2200,
    "allergies": [],
    "food_preferences": ["Indian food"],
    "meals_per_day": 4
}

try:
    result = generate_meal_plan(user_profile)

    print("\nMEAL PLAN GENERATION RESULT")
    print("=" * 50)
    print(result)

    print("\nMeal planner test completed!")

except Exception as error:
    print("Error:", error)
