from openai import OpenAI
import os
import random
from functools import lru_cache
from sqlalchemy.orm import Session
from database import get_db_session, Recipe, Ingredient, UserSearch, SuggestedRecipe
from datetime import datetime

class RecipeRecommender:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)
        print(f"API Key: {self.api_key[:5]}...")
        print("OpenAI API key successfully set.")

    def get_cached_recipe(self, db: Session, ingredients, cuisine=None, strict=False):
        ingredients_set = set(ingredients)
        recipes = db.query(Recipe).filter(Recipe.cuisine == cuisine if cuisine else True).all()
        
        for recipe in recipes:
            recipe_ingredients = set(ing.name.lower() for ing in recipe.ingredients)
            if strict:
                if ingredients_set == recipe_ingredients:
                    return recipe
            elif ingredients_set.issubset(recipe_ingredients):
                return recipe
        return None

    @lru_cache(maxsize=100)
    def generate_recipe(self, db: Session, ingredients_tuple, cuisine=None, strict=False, suggest=False, language='en'):
        ingredients = list(ingredients_tuple)
        print(f"Generating recipe for ingredients: {', '.join(ingredients)}")

        # Check for cached recipe
        cached_recipe = self.get_cached_recipe(db, ingredients, cuisine, strict)
        if cached_recipe:
            return self._recipe_to_dict(cached_recipe)

        if language == 'en':
            prompt = f"Create a recipe using the following ingredients: {', '.join(ingredients)}."
            if strict:
                prompt += " Use only these ingredients and nothing else."
            elif suggest:
                prompt += " You may suggest additional ingredients to enhance the recipe."
            prompt += " Include the recipe name, ingredients list, and instructions."
            if cuisine and cuisine != "Any":
                prompt += f" The cuisine type should be {cuisine}."
            system_message = "You are a helpful assistant that creates recipes."
        elif language == 'tr':
            prompt = f"Şu malzemeleri kullanarak bir tarif oluşturun: {', '.join(ingredients)}."
            if strict:
                prompt += " Sadece bu malzemeleri kullanın, başka bir şey eklemeyin."
            elif suggest:
                prompt += " Tarifi geliştirmek için ek malzemeler önerebilirsiniz."
            prompt += " Tarif adını, malzeme listesini ve talimatları dahil edin."
            if cuisine and cuisine != "Any":
                prompt += f" Mutfak türü {cuisine} olmalıdır."
            system_message = "Siz tarif oluşturan yardımcı bir asistansınız."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
            )
            
            recipe_text = response.choices[0].message.content.strip()
            print(f"Generated recipe text:\n{recipe_text}")  # Debug print
            parsed_recipe = self._parse_recipe(recipe_text, language)
            print(f"Parsed recipe (language: {language}): {parsed_recipe}")  # Debug print
            self._save_recipe_to_db(db, parsed_recipe, ingredients)
            return parsed_recipe
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return self._fallback_recipe(db, ingredients, cuisine)

    def _parse_recipe(self, recipe_text, language):
        lines = recipe_text.split('\n')
        recipe = {
            'name': '',
            'ingredients': [],
            'instructions': [],
            'cuisine': ''
        }
        
        section = ''
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if not recipe['name']:
                recipe['name'] = line
                continue
            
            if language == 'en':
                if line.lower().startswith('ingredients:'):
                    section = 'ingredients'
                    continue
                elif line.lower().startswith('instructions:'):
                    section = 'instructions'
                    continue
                elif line.lower().startswith('cuisine:'):
                    recipe['cuisine'] = line.split(':')[1].strip()
                    continue
            elif language == 'tr':
                if line.lower().startswith('malzemeler:'):
                    section = 'ingredients'
                    continue
                elif line.lower().startswith('talimatlar:') or line.lower().startswith('hazırlanışı:'):
                    section = 'instructions'
                    continue
                elif line.lower().startswith('mutfak:'):
                    recipe['cuisine'] = line.split(':')[1].strip()
                    continue
            
            if section == 'ingredients':
                recipe['ingredients'].append(line.lstrip('- '))
            elif section == 'instructions':
                recipe['instructions'].append(line.lstrip('1234567890. '))
        
        return recipe

    def _save_recipe_to_db(self, db: Session, recipe_dict, input_ingredients):
        new_recipe = Recipe(name=recipe_dict['name'], instructions='\n'.join(recipe_dict['instructions']), cuisine=recipe_dict['cuisine'])
        db.add(new_recipe)
        
        for ing_name in recipe_dict['ingredients']:
            ingredient = db.query(Ingredient).filter(Ingredient.name == ing_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ing_name)
                db.add(ingredient)
            new_recipe.ingredients.append(ingredient)
        
        db.commit()

    def _fallback_recipe(self, db: Session, ingredients, cuisine=None):
        recipes = db.query(Recipe).filter(Recipe.cuisine == cuisine if cuisine else True).all()
        matching_recipes = []

        for recipe in recipes:
            recipe_ingredients = set(ing.name.lower() for ing in recipe.ingredients)
            if any(ing.lower() in recipe_ingredients for ing in ingredients):
                matching_recipes.append(recipe)

        if matching_recipes:
            chosen_recipe = random.choice(matching_recipes)
            return self._recipe_to_dict(chosen_recipe)
        else:
            return None

    def _recipe_to_dict(self, recipe):
        return {
            'name': recipe.name,
            'ingredients': [ing.name for ing in recipe.ingredients],
            'instructions': recipe.instructions.split('\n'),
            'cuisine': recipe.cuisine
        }

    def recommend_recipe(self, db: Session, ingredients, cuisine=None, strict=False, suggest=False, language='en'):
        ingredients_tuple = tuple(sorted(ingredients))
        recipe = self.generate_recipe(db, ingredients_tuple, cuisine, strict, suggest, language)
        
        if recipe:
            # Log user search and suggested recipe
            user_search = UserSearch(search_query=','.join(ingredients), timestamp=datetime.now().isoformat())
            db.add(user_search)
            db.commit()

            db_recipe = db.query(Recipe).filter(Recipe.name == recipe['name']).first()
            if db_recipe:
                suggested_recipe = SuggestedRecipe(search_id=user_search.id, recipe_id=db_recipe.id)
                db.add(suggested_recipe)
                db.commit()

        return recipe

# Create a global instance of RecipeRecommender
recommender = RecipeRecommender()
