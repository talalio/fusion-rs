import pandas as pd
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# Load the data
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# Create a user-item ratings matrix
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# Apply Non-negative Matrix Factorization (NMF)
nmf = NMF(n_components=20, max_iter=1500, random_state=42)
user_factors = nmf.fit_transform(user_item_matrix)
item_factors = nmf.components_

# Compute cosine similarity for item factors
movie_similarity = cosine_similarity(item_factors.T)

def get_movie_id_from_title(movie_title):
    """
    Find the closest matching movie title using fuzzy matching.
    
    Args:
    - movie_title (str): The name of the movie input by the user.
    
    Returns:
    - movie_id (int): The ID of the closest matching movie.
    """
    choices = movies['title'].tolist()
    closest_match = process.extractOne(movie_title, choices)
    if closest_match:
        match_title = closest_match[0]
        movie_id = movies[movies['title'] == match_title]['movieId'].values[0]
        print(f"Matched input to: '{match_title}' (Movie ID: {movie_id})")
        return movie_id
    else:
        raise ValueError("No close match found for the movie title.")

def recommend_movies_by_title(movie_title, top_n=10):
    """
    Recommend movies based on the title of a given movie, excluding the input movie itself.
    
    Args:
    - movie_title (str): Title of the movie to base recommendations on.
    - top_n (int): Number of recommendations to return.
    
    Returns:
    - List of recommended movie titles.
    """
    movie_id = get_movie_id_from_title(movie_title)
    movie_index = movies[movies['movieId'] == movie_id].index[0]
    
    similarity_scores = list(enumerate(movie_similarity[movie_index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Filter out the matched movie's own index
    recommended_movie_indices = [i[0] for i in sorted_scores if i[0] != movie_index][:top_n]
    
    recommended_movies = movies.iloc[recommended_movie_indices]['title'].tolist()
    return recommended_movies

# Prompt the user for input
user_input = input("Enter the name of a movie you like: ")
recommendations = recommend_movies_by_title(user_input, top_n=10)

# Display recommendations
print("\nRecommendations based on your input:")
for idx, title in enumerate(recommendations, start=1):
    print(f"{idx}. {title}")
