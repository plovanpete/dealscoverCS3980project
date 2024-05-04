 // Function to add a new recipe button
function addRecipe() {
    var gridContainer = document.getElementById("gridContainer");
    var newGridItem = document.createElement("div");
    newGridItem.classList.add("grid-item");
    newGridItem.innerHTML = "<button>Recipe " + (gridContainer.children.length + 1) + "</button>";
    //gridContainer.appendChild(newGridItem);
}

// Event listener for the add recipe button
document.getElementById("addRecipeBtn").addEventListener("click", addRecipe);