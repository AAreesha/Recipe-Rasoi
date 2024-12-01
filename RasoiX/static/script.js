document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript loaded and DOM is ready.");

    const form = document.getElementById('recommendation-form');
    if (!form) {
        console.error("Recommendation form not found!");
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log("Form submission intercepted.");

        const formData = new FormData(this);
        console.log("Form data created:", Array.from(formData.entries()));

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                console.error("Failed to fetch recommendations. Status:", response.status);
                document.getElementById('recommendations').innerHTML = "<p>Error fetching recommendations.</p>";
                return;
            }

            const recommendations = await response.json();
            console.log("Recommendations received:", recommendations);

            const recommendationsDiv = document.getElementById('recommendations');
            recommendationsDiv.innerHTML = "";

            if (recommendations.length === 0) {
                recommendationsDiv.innerHTML = "<p>No recommendations found.</p>";
                return;
            }

            recommendations.forEach((rec, index) => {
                console.log(`Rendering recommendation ${index + 1}:`, rec);
                const recDiv = document.createElement('div');
                recDiv.classList.add('recommendation');
                recDiv.innerHTML = `
                    <h2>${index + 1}. ${rec.name}</h2>
                    <p><strong>Ingredients:</strong> ${rec.ingredients}</p>
                    <p><strong>Region:</strong> ${rec.region}</p>
                    <p><strong>Cooking Method:</strong> ${rec.method}</p>
                    <p><strong>Category:</strong> ${rec.category}</p>
                    <p><strong>Recipe:</strong> ${rec.recipe}</p>
                `;
                recommendationsDiv.appendChild(recDiv);
            });
        } catch (error) {
            console.error("Error:", error);
            document.getElementById('recommendations').innerHTML = "<p>There was an error processing your request.</p>";
        }
    });
});
