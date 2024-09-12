"""Database models and connection utilities."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

# Use SQLite database
DATABASE_URL = "sqlite:///./recipe_recommender.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base class for declarative models
Base = declarative_base()

# Define the association table for Recipe-Ingredient relationship
recipe_ingredient = Table(
    'recipe_ingredient', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

class Ingredient(Base):
    """Represents an ingredient in the database."""
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    recipes = relationship("Recipe", secondary=recipe_ingredient, back_populates="ingredients")

    def __repr__(self) -> str:
        return f"<Ingredient(name='{self.name}')>"

class Recipe(Base):
    """Represents a recipe in the database."""
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    instructions = Column(String)
    cuisine = Column(String, index=True)
    ingredients = relationship("Ingredient", secondary=recipe_ingredient, back_populates="recipes")

    def __repr__(self) -> str:
        return f"<Recipe(name='{self.name}', cuisine='{self.cuisine}')>"

class UserSearch(Base):
    """Represents a user search in the database."""
    __tablename__ = 'user_searches'
    id = Column(Integer, primary_key=True)
    search_query = Column(String)
    timestamp = Column(String)
    suggested_recipes = relationship("SuggestedRecipe", back_populates="user_search")

    def __repr__(self) -> str:
        return f"<UserSearch(query='{self.search_query}', timestamp='{self.timestamp}')>"

class SuggestedRecipe(Base):
    """Represents a suggested recipe in the database."""
    __tablename__ = 'suggested_recipes'
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('user_searches.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    user_search = relationship("UserSearch", back_populates="suggested_recipes")
    recipe = relationship("Recipe")

    def __repr__(self) -> str:
        return f"<SuggestedRecipe(search_id={self.search_id}, recipe_id={self.recipe_id})>"

class User(Base):
    """Represents a user in the database."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
