async function createRecipe() {
    const title = document.getElementById('recipeTitle').value;
    const description = document.getElementById('recipeDescription').value;
    const imageFile = document.getElementById('recipeImage').files[0];

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    
    // Check if imageFile is not null before appending
    if (imageFile) {
        formData.append('image', imageFile);
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/recipes/', {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Failed to create recipe');
        }
        // Refresh recipes after creating a new one
        fetchRecipes();
        // Close the modal
        $('#addRecipeModal').modal('hide');
    } catch (error) {
        console.error('Error creating recipe:', error);
        // Handle error, e.g., show an error message to the user
    }
}


// Event listener for creating a recipe
document.getElementById('createRecipeBtn').addEventListener('click', createRecipe);

// Function to fetch recipes from the backend
async function fetchRecipes() {
    try {
        const response = await fetch('http://127.0.0.1:8000/allrecipes/');
        if (!response.ok) {
            throw new Error('Failed to fetch recipes');
        }
        const recipes = await response.json();
        renderRecipes(recipes);
    } catch (error) {
        console.error('Error fetching recipes:', error);
        // Handle error
    }
}

// Function to render recipes
function renderRecipes(recipes) {
    const recipeGrid = document.getElementById('recipeGrid');
    recipeGrid.innerHTML = ''; // Clear previous content

    recipes.forEach(recipe => {
        const cardDiv = document.createElement('div');
        cardDiv.classList.add('col-md-4');
        cardDiv.innerHTML = `
            <div class="card mb-4 shadow-sm">
                <img src="${recipe.imageUrl}" class="card-img-top" alt="Recipe Image">
                <div class="card-body">
                    <h5 class="card-title">${recipe.title}</h5>
                    <p class="card-text">${recipe.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="btn-group">
                            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="onViewRecipe('${recipe.title}', '${recipe.description}', '${recipe.imageUrl}')">View</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        recipeGrid.appendChild(cardDiv);
    });
}

// Function to handle click event of "View" button
function onViewRecipe(title, description, imageUrl) {
    // Update modal with recipe details
    document.getElementById('viewRecipeTitle').textContent = title;
    document.getElementById('viewRecipeDescription').textContent = description;
    document.getElementById('viewRecipeImage').src = imageUrl;

    // Show the modal
    $('#viewRecipeModal').modal('show');
}

// Call fetchRecipes when the page loads to initially populate the recipe grid
window.addEventListener('load', fetchRecipes);


