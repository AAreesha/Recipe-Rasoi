from flask import Flask, request, jsonify, render_template
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load recipe data from Excel
file_path = "groundfinal.xlsx"
recipe_df = pd.read_excel(file_path)

# Combine recipe details into a single string for each recipe
recipe_df['combined_text'] = (
    recipe_df['Ingredients'] + " | " +
    recipe_df['Cuisine Region'] + " | " +
    recipe_df['Cooking Method'] + " | " +
    recipe_df['Recipe']
)

# Convert the combined text to a list
recipes = recipe_df['combined_text'].tolist()

# Initialize SentenceTransformer
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

@app.route('/')
def index():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    user_input = data['user_input']
    cuisine_region = data['cuisine_region']
    cooking_method = data['cooking_method']

    # Process user input
    user_input_embedding = sentence_model.encode([user_input])
    recipe_embeddings = sentence_model.encode(recipes)
    cosine_sim = cosine_similarity(user_input_embedding, recipe_embeddings)
    
    top_n = 5
    top_indices = np.argsort(cosine_sim[0])[-top_n:][::-1]
    top_recipes = [recipe_df.iloc[idx]['Recipe Name'] for idx in top_indices]

    # Return the recommendations
    return jsonify({'recommendations': top_recipes})

if __name__ == '__main__':
    app.run(debug=True)
