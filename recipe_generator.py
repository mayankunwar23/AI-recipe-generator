import data
import random

class RecipeGenerator:
    def __init__(self):
        # Load recipes safely
        try:
            self.recipes = data.load_recipes()
            if "recipes" not in self.recipes:
                raise ValueError("Invalid recipe data format")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading recipes: {e}")
            self.recipes = {"recipes": []}  # Fallback to empty list

    def generate_recipe(self):
        """Return a random recipe from the dataset."""
        if not self.recipes["recipes"]:
            return "No recipes available."
        return random.choice(self.recipes["recipes"])

    def suggest_recipe(self, preferences):
        """
        Suggest a recipe based on user preferences.
        Example preference: {"diet": "vegetarian", "cuisine": "Italian"}
        """
        if not self.recipes["recipes"]:
            return "No recipes available."

        filtered_recipes = [
            recipe for recipe in self.recipes["recipes"]
            if all(pref in recipe.get("tags", []) for pref in preferences.values())
        ]

        return random.choice(filtered_recipes) if filtered_recipes else "No matching recipes found."

    def substitute_ingredient(self, ingredient):
        """Suggest a substitute for a given ingredient."""
        substitutions = {
            "milk": "almond milk",
            "butter": "olive oil",
            "sugar": "honey",
            "flour": "almond flour",
            "egg": "flaxseed meal + water"
        }

        return substitutions.get(ingredient.lower(), f"No substitute found for {ingredient}.")

