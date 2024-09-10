import pandas as pd

class RecipeManager:
    """Manages recipes using a pandas DataFrame."""

    def __init__(self, csv_file: str):
        self.recipes_df = pd.read_csv(csv_file)

    def get_recipes(self) -> pd.DataFrame:
        """Return all recipes."""
        return self.recipes_df

    def get_recipe_by_name(self, name: str) -> pd.Series:
        """Return a recipe by its name."""
        return self.recipes_df[self.recipes_df['name'] == name].iloc[0]

    def get_recipes_by_cuisine(self, cuisine: str) -> pd.DataFrame:
        """Return recipes filtered by cuisine."""
        return self.recipes_df[self.recipes_df['cuisine'] == cuisine]

    def add_recipe(self, name: str, ingredients: str, instructions: str, cuisine: str):
        """Add a new recipe to the DataFrame."""
        new_recipe = pd.DataFrame({
            'name': [name],
            'ingredients': [ingredients],
            'instructions': [instructions],
            'cuisine': [cuisine]
        })
        self.recipes_df = pd.concat([self.recipes_df, new_recipe], ignore_index=True)

    def save_recipes(self, csv_file: str):
        """Save the recipes DataFrame to a CSV file."""
        self.recipes_df.to_csv(csv_file, index=False)
