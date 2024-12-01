from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from flask import url_for
app = Flask(__name__)

# Load recipe data
file_path = "groundfinal.xlsx"  # Ensure the file path is correct and accessible
try:
    recipe_df = pd.read_excel(file_path)
except Exception as e:
    raise FileNotFoundError(f"Failed to load {file_path}: {e}")

# Ensure required columns exist
required_columns = ['Ingredients', 'Cuisine Region', 'Cooking Method', 'Recipe', 'Recipe Name', 'Category']
missing_columns = [col for col in required_columns if col not in recipe_df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns in the dataset: {missing_columns}")

# Combine text for embeddings
recipe_df['combined_text'] = (
    recipe_df['Ingredients'].fillna('') + " | " +
    recipe_df['Cuisine Region'].fillna('') + " | " +
    recipe_df['Cooking Method'].fillna('') + " | " +
    recipe_df['Recipe'].fillna('')
)

# Initialize models
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Embed recipes
recipe_embeddings = sentence_model.encode(recipe_df['combined_text'].tolist(), show_progress_bar=True)
recipe_names = recipe_df['Recipe Name'].tolist()


def recommend_recipes(user_input, filters, top_n=5):
    filtered_df = recipe_df.copy()

    # Apply optional filters
    if filters.get("cuisine"):
        filtered_df = filtered_df[
            filtered_df['Cuisine Region']
            .str.contains(filters['cuisine'], case=False, na=False)
        ]
    if filters.get("category"):
        filtered_df = filtered_df[
            filtered_df['Category']
            .str.contains(filters['category'], case=False, na=False)
        ]

    if filtered_df.empty:
        return []

    # Score recipes
    recipes = filtered_df['combined_text'].tolist()
    recipe_names = filtered_df['Recipe Name'].tolist()
    recipe_embeddings = sentence_model.encode(recipes)

    # Generate cross scores
    recipe_pairs = [(user_input, recipe) for recipe in recipes]
    cross_scores = cross_encoder.predict(recipe_pairs)

    # Get top N recommendations
    top_indices = np.argsort(cross_scores)[-top_n:][::-1]
    top_recipes = [
        {
            "name": recipe_names[idx],
            "ingredients": filtered_df.iloc[idx]['Ingredients'],
            "region": filtered_df.iloc[idx]['Cuisine Region'],
            "method": filtered_df.iloc[idx]['Cooking Method'],
            "category": filtered_df.iloc[idx]['Category'],
            "recipe": filtered_df.iloc[idx]['Recipe']
        }
        for idx in top_indices
    ]
    return top_recipes


@app.route('/')
def index():
    cuisines = recipe_df['Cuisine Region'].dropna().unique()
    categories = recipe_df['Category'].dropna().unique()
    return render_template('index.html', cuisines=cuisines, categories=categories)
    
    print(url_for('static', filename='style.css'))
    print(url_for('static', filename='script.js'))



@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input', '').strip()
    filters = {
        "cuisine": request.form.get('cuisine', '').strip(),
        "category": request.form.get('category', '').strip()
    }
    recommendations = recommend_recipes(user_input, filters)
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
