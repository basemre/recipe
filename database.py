"""This module defines the database models and provides database connection utilities."""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
    """Represents an ingredient in the database."""
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    recipes = relationship("Recipe", secondary=recipe_ingredient, back_populates="ingredients")

class Recipe(Base):
    """Represents a recipe in the database."""
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    instructions = Column(String)
    cuisine = Column(String, index=True)
    ingredients = relationship("Ingredient", secondary=recipe_ingredient, back_populates="recipes")

class UserSearch(Base):
    """Represents a user search in the database."""
    __tablename__ = 'user_searches'
    id = Column(Integer, primary_key=True)
    search_query = Column(String)
    timestamp = Column(String)
    suggested_recipes = relationship("SuggestedRecipe", back_populates="user_search")

class SuggestedRecipe(Base):
    """Represents a suggested recipe in the database."""
    __tablename__ = 'suggested_recipes'
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('user_searches.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    user_search = relationship("UserSearch", back_populates="suggested_recipes")
    recipe = relationship("Recipe")

class User(Base):
    """Represents a user in the database."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """
    Provides a transactional scope around a series of operations.
    
    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
