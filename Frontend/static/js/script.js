document.getElementById("recipe-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    // Get user input and selected values from dropdowns
    let userInput = document.getElementById("user-input").value;
    let cuisineRegion = document.getElementById("cuisine-region").value;
    let cookingMethod = document.getElementById("cooking-method").value;

    console.log("User Input:", userInput);
    console.log("Cuisine Region:", cuisineRegion);
    console.log("Cooking Method:", cookingMethod);

    // Send POST request to Flask API
    fetch('/get-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_input: userInput,
            cuisine_region: cuisineRegion,
            cooking_method: cookingMethod
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received Response:", data);  // Log the response from the Flask API
        // Handle the response (e.g., display recommended recipes)
        if (data.recommendations && data.recommendations.length > 0) {
            const recommendationsList = document.getElementById("recommendations-list");
            recommendationsList.innerHTML = '';  // Clear previous recommendations
            data.recommendations.forEach(recipe => {
                const listItem = document.createElement("li");
                listItem.textContent = recipe;
                recommendationsList.appendChild(listItem);
            });
        } else {
            console.log("No recommendations found.");
        }
    })
    .catch(error => console.error('Error:', error));
});
