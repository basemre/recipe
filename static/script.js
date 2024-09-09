document.addEventListener('DOMContentLoaded', () => {
    const getRecipeButton = document.getElementById('getRecipe');
    const strictIngredientsButton = document.getElementById('strictIngredients');
    const suggestIngredientsButton = document.getElementById('suggestIngredients');
    const ingredientsInput = document.getElementById('ingredients');
    const cuisineSelect = document.getElementById('cuisine');
    const langButtons = document.querySelectorAll('.lang-btn');
    const recipeResult = document.getElementById('recipeResult');
    const recipeName = document.getElementById('recipeName');
    const recipeIngredients = document.getElementById('recipeIngredients');
    const recipeInstructions = document.getElementById('recipeInstructions');

    let currentLanguage = 'en';

    function updateLanguage(lang) {
        currentLanguage = lang;
        langButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });
        const langData = translations[currentLanguage];
        document.querySelector('h1').textContent = langData.title;
        document.querySelector('header h2').textContent = langData.subtitle;
        document.querySelector('.input-section h3').textContent = langData.ingredientsLabel;
        getRecipeButton.textContent = langData.getRecipe;
        strictIngredientsButton.textContent = langData.strictIngredients;
        suggestIngredientsButton.textContent = langData.suggestIngredients;
        document.querySelector('footer p:first-child').textContent = langData.socialMedia;
        document.querySelector('footer p:last-child').textContent = langData.copyright;

        // Update placeholder
        ingredientsInput.placeholder = langData.placeholderIngredients;

        // Update cuisine options
        const cuisineOptions = cuisineSelect.querySelectorAll('option');
        cuisineOptions.forEach(option => {
            const translateKey = option.getAttribute('data-translate');
            if (translateKey) {
                option.textContent = langData[translateKey];
            }
        });
    }

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => updateLanguage(btn.dataset.lang));
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
