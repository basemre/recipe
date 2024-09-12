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
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const mainContent = document.querySelector('main');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginSubmit = document.getElementById('loginSubmit');
    const signupSubmit = document.getElementById('signupSubmit');

    updateLanguage();

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

    function showLoginForm() {
        mainContent.style.display = 'none';
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    }

    function showSignupForm() {
        mainContent.style.display = 'none';
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
    }

    function showMainContent() {
        mainContent.style.display = 'block';
        loginForm.style.display = 'none';
        signupForm.style.display = 'none';
    }

    loginBtn.addEventListener('click', showLoginForm);
    signupBtn.addEventListener('click', showSignupForm);

    document.getElementById('goToSignup').addEventListener('click', (e) => {
        e.preventDefault();
        showSignupForm();
    });

    document.getElementById('goToLogin').addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });

    function updateAuthUI() {
        if (auth.isAuthenticated()) {
            loginBtn.style.display = 'none';
            signupBtn.style.display = 'none';
            logoutBtn.style.display = 'inline-block';
            showMainContent();
        } else {
            loginBtn.style.display = 'inline-block';
            signupBtn.style.display = 'inline-block';
            logoutBtn.style.display = 'none';
            showLoginForm();
        }
    }

    // Check auth status on page load
    auth.checkAuthStatus().then(updateAuthUI);

    loginSubmit.addEventListener('click', async (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        try {
            await auth.login(username, password);
            updateAuthUI();
        } catch (error) {
            alert('Login failed. Please try again.');
        }
    });

    signupSubmit.addEventListener('click', async (e) => {
        e.preventDefault();
        const username = document.getElementById('signupUsername').value;
        const password = document.getElementById('signupPassword').value;
        try {
            await signup(username, password);
            alert('Signup successful. Please log in.');
            showLoginForm();
        } catch (error) {
            alert('Signup failed. Please try again.');
        }
    });

    logoutBtn.addEventListener('click', () => {
        auth.logout();
        updateAuthUI();
    });
});
