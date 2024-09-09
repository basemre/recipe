import pandas as pd

class RecipeManager:
    def __init__(self, csv_file):
        self.recipes_df = pd.read_csv(csv_file)
        
    def get_recipes(self):
        return self.recipes_df
    
    def get_recipe_by_name(self, name):
        return self.recipes_df[self.recipes_df['name'] == name].iloc[0]
    
    def get_recipes_by_cuisine(self, cuisine):
        return self.recipes_df[self.recipes_df['cuisine'] == cuisine]
    
    def add_recipe(self, name, ingredients, instructions, cuisine):
        new_recipe = pd.DataFrame({
            'name': [name],
            'ingredients': [ingredients],
            'instructions': [instructions],
            'cuisine': [cuisine]
        })
        self.recipes_df = pd.concat([self.recipes_df, new_recipe], ignore_index=True)
        
    def save_recipes(self, csv_file):
        self.recipes_df.to_csv(csv_file, index=False)
