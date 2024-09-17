"""Main application module for the Recipe Recommender."""

from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv
from model import recommender
from database import get_db_session, Recipe, Ingredient, UserSearch, SuggestedRecipe

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/auth/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Set a secret key for session management
app.secret_key = os.getenv('SECRET_KEY')

# Database setup
def get_db_connection():
    conn = sqlite3.connect('recipe_recommender.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create users table if it doesn't exist
def create_users_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL)''')
    conn.close()

create_users_table()

@app.route('/')
def index():
    """Serve the main page of the application."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/recipe', methods=['POST'])
def get_recipe():
    """Handle recipe generation requests."""
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
    return jsonify({'error': 'Unable to generate a recipe'}), 400

@app.route('/auth/register', methods=['POST'])
def register():
    print("Received registration request")
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                     (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return jsonify({"message": "Login successful", "user_id": user['id']}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/auth/user', methods=['GET'])
def get_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    conn = get_db_connection()
    user = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return jsonify({"id": user['id'], "username": user['username']}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
