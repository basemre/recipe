import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from contextlib import contextmanager

# Get the database URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Define the association table for Recipe-Ingredient relationship
recipe_ingredient = Table('recipe_ingredient', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    instructions = Column(String)
    cuisine = Column(String, index=True)
    ingredients = relationship("Ingredient", secondary=recipe_ingredient, back_populates="recipes")

class UserSearch(Base):
    __tablename__ = 'user_searches'
    id = Column(Integer, primary_key=True)
    search_query = Column(String)
    timestamp = Column(String)

class SuggestedRecipe(Base):
    __tablename__ = 'suggested_recipes'
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('user_searches.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    user_search = relationship("UserSearch", back_populates="suggested_recipes")
    recipe = relationship("Recipe")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)

# Add back_populates to Ingredient class
Ingredient.recipes = relationship("Recipe", secondary=recipe_ingredient, back_populates="ingredients")

# Add back_populates to UserSearch class
UserSearch.suggested_recipes = relationship("SuggestedRecipe", back_populates="user_search")

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
