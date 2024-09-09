# Recipe Recommender
A web application that suggests recipes based on available ingredients, using machine learning for personalized recommendations.
## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Setup Instructions](#setup-instructions)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Database Schema](#database-schema)
9. [Debugging](#debugging)
10. [Further Development](#further-development)
## Project Overview
The Recipe Recommender is a Flask-based web application that uses OpenAI's GPT-3.5 model to generate recipe suggestions based on user-provided ingredients. It supports both English and Turkish languages and offers features like strict ingredient usage and additional ingredient suggestions.
## Features
- Recipe generation based on input ingredients
- Support for English and Turkish languages
- Strict ingredient mode (use only provided ingredients)
- Suggestion mode (recommend additional ingredients)
- Caching of generated recipes for improved performance
- Responsive web interface
## Tech Stack
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL (with SQLAlchemy ORM)
- AI Model: OpenAI GPT-3.5
- Additional Libraries: pandas
## Project Structure
.
├── .streamlit/
│ └── config.toml
├── data/
│ └── recipes.csv
├── static/
│ ├── index.html
│ ├── script.js
│ ├── style.css
│ └── translations.js
├── database.py
├── main.py
├── model.py
├── recipe_manager.py
├── requirements.txt
└── README.md

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/your-username/recipe-recommender.git
   cd recipe-recommender
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following variables:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Initialize the database:
   ```python
   from database import Base, engine
   Base.metadata.create_all(engine)
   ```

6. Run the application:
   ```
   python main.py
   ```

The application should now be running on `http://localhost:5000`.
## Usage
1. Open the application in a web browser.
2. Enter ingredients in the input field (comma-separated).
3. Select a cuisine type (optional).
4. Choose the language (English or Turkish).
5. Click "Get Recipe" for a standard recommendation.
6. Use "Use Only These Ingredients" for strict mode.
7. Use "Suggest Additional Ingredients" for suggestions.
## API Endpoints
- `POST /api/recipe`: Generate a recipe
- Request body: `{ "ingredients": string, "cuisine": string, "strict": boolean, "suggest": boolean, "language": string }`
- Response: Recipe object or error message
## Database Schema
- Ingredients: id, name
- Recipes: id, name, instructions, cuisine
- UserSearches: id, search_query, timestamp
- SuggestedRecipes: id, search_id, recipe_id
- Users: id, username, email
## Debugging
1. Check the console output for error messages and API responses.
2. Use the debug print statements in the `model.py` file to track the recipe generation process.
3. Verify the database connection and API key setup in the environment variables.
## Further Development
1. Implement user authentication and authorization.
2. Add a feature for users to save favorite recipes.
3. Integrate nutritional information for suggested recipes.
4. Implement a rating and review system for recipes.
5. Expand language support to include more languages.
6. Optimize the recipe generation algorithm for better performance.
7. Implement unit and integration tests for the application.
For any issues or feature requests, please open an issue on the GitHub repository.