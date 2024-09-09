from flask import Flask, request, jsonify, send_from_directory
from model import recommender
from database import get_db_session

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/recipe', methods=['POST'])
def get_recipe():
    data = request.json
    ingredients = [ing.strip().lower() for ing in data['ingredients'].split(',')]
    cuisine = data['cuisine'] if data['cuisine'] != 'Any' else None
    strict = data.get('strict', False)
    suggest = data.get('suggest', False)
    language = data.get('language', 'en')

    with get_db_session() as db:
        recipe = recommender.recommend_recipe(db, ingredients, cuisine, strict, suggest, language)

    if recipe:
        return jsonify(recipe)
    else:
        return jsonify({'error': 'Unable to generate a recipe'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
