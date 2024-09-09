document.addEventListener('DOMContentLoaded', () => {
    const getRecipeButton = document.getElementById('getRecipe');
    const strictIngredientsButton = document.getElementById('strictIngredients');
    const suggestIngredientsButton = document.getElementById('suggestIngredients');
    const ingredientsInput = document.getElementById('ingredients');
    const cuisineSelect = document.getElementById('cuisine');
    const languageSelect = document.getElementById('language');
    const recipeResult = document.getElementById('recipeResult');
    const recipeName = document.getElementById('recipeName');
    const recipeIngredients = document.getElementById('recipeIngredients');
    const recipeInstructions = document.getElementById('recipeInstructions');

    let currentLanguage = 'en';

    function updateLanguage() {
        const lang = translations[currentLanguage];
        document.querySelector('h1').textContent = lang.title;
        document.querySelector('header p').textContent = lang.subtitle;
        document.querySelector('.input-section h2').textContent = lang.ingredientsLabel;
        getRecipeButton.textContent = lang.getRecipe;
        strictIngredientsButton.textContent = lang.strictIngredients;
        suggestIngredientsButton.textContent = lang.suggestIngredients;
        document.querySelector('footer p:first-child').textContent = lang.socialMedia;
        document.querySelector('footer p:last-child').textContent = lang.copyright;
    }

    languageSelect.addEventListener('change', (event) => {
        currentLanguage = event.target.value;
        updateLanguage();
    });

    function getRecipe(strict = false, suggest = false) {
        const ingredients = ingredientsInput.value;
        const cuisine = cuisineSelect.value;

        if (ingredients) {
            fetch('/api/recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients, cuisine, strict, suggest }),
            })
            .then(response => response.json())
            .then(recipe => {
                recipeName.textContent = recipe.name;
                recipeIngredients.innerHTML = recipe.ingredients.map(ing => `<li>${ing}</li>`).join('');
                recipeInstructions.innerHTML = recipe.instructions.map(inst => `<li>${inst}</li>`).join('');
                recipeResult.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Unable to generate a recipe. Please try again with different ingredients or cuisine type.');
            });
        } else {
            alert('Please enter some ingredients before getting a recipe.');
        }
    }

    getRecipeButton.addEventListener('click', () => getRecipe());
    strictIngredientsButton.addEventListener('click', () => getRecipe(true, false));
    suggestIngredientsButton.addEventListener('click', () => getRecipe(false, true));

    updateLanguage();
});
