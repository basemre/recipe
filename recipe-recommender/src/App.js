import React, { useState, useEffect } from 'react';
import { Search, ChefHat, X, LogIn, LogOut, UserPlus } from 'lucide-react';
import Button from './components/Button';
import Input from './components/Input';
import Card from './components/Card';

const API_BASE_URL = 'http://localhost:5000';

const RecipeRecommender = () => {
  const [ingredients, setIngredients] = useState([]);
  const [currentIngredient, setCurrentIngredient] = useState('');
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [cuisine, setCuisine] = useState('Any');
  const [strict, setStrict] = useState(false);
  const [suggest, setSuggest] = useState(false);
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/user`, {
        credentials: 'include'
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error('Error checking user:', error);
    }
  };

  const addIngredient = () => {
    if (currentIngredient.trim() !== '' && !ingredients.includes(currentIngredient.trim())) {
      setIngredients([...ingredients, currentIngredient.trim()]);
      setCurrentIngredient('');
    }
  };

  const removeIngredient = (ingredient) => {
    setIngredients(ingredients.filter(ing => ing !== ingredient));
  };

  const generateRecipe = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/recipe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ingredients: ingredients.join(','),
          cuisine,
          strict,
          suggest,
          language
        }),
        credentials: 'include'
      });
      
      if (response.ok) {
        const recipeData = await response.json();
        setRecipe(recipeData);
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to generate recipe');
      }
    } catch (error) {
      setError('An error occurred while generating the recipe');
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      
      if (response.ok) {
        setError('');
        await handleLogin();
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Registration failed');
      }
    } catch (error) {
      setError('An error occurred during registration');
    }
  };

  const handleLogin = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Login failed');
      }
    } catch (error) {
      setError('An error occurred during login');
    }
  };

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
      
      if (response.ok) {
        setUser(null);
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Logout failed');
      }
    } catch (error) {
      setError('An error occurred during logout');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-100 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-600">Recipe Recommender</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {user ? (
        <div className="mb-4 flex justify-between items-center">
          <span>Welcome, {user.username}!</span>
          <Button onClick={handleLogout} className="bg-red-500 hover:bg-red-600">
            <LogOut className="mr-2" /> Logout
          </Button>
        </div>
      ) : (
        <div className="mb-4 flex space-x-2">
          <Input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <Button onClick={handleLogin} className="bg-green-500 hover:bg-green-600">
            <LogIn className="mr-2" /> Login
          </Button>
          <Button onClick={handleRegister} className="bg-blue-500 hover:bg-blue-600">
            <UserPlus className="mr-2" /> Register
          </Button>
        </div>
      )}
      
      {/* Add the rest of your JSX here */}
    </div>
  );
};

export default RecipeRecommender;