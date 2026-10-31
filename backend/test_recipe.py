
from services.recipe_ai import generate_recipe

try:
    result = generate_recipe(
        text_input="Paneer Butter Masala"
    )

    print("\nSMART KITCHEN RECIPE")
    print("-" * 40)

    print("Dish:", result["dish_name"])
    print("Description:", result["description"])
    print("Preparation Time:", result["preparation_time"])
    print("Cooking Time:", result["cooking_time"])
    print("Difficulty:", result["difficulty"])
    print("Servings:", result["servings"])

    print("\nINGREDIENTS")

    for ingredient in result["ingredients"]:
        print(
            f"- {ingredient['name']}: "
            f"{ingredient['quantity']}"
        )

    print("\nCOOKING STEPS")

    for step in result["steps"]:
        print(
            f"{step['step']}. {step['instruction']} "
            f"({step['duration']})"
        )

    print("\nCOOKING TIPS")

    for tip in result["cooking_tips"]:
        print("-", tip)

    print("\nRecipe generation completed!")

except Exception as error:
    print("Error:", error)
