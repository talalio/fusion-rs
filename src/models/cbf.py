import pandas as pd
from operator import itemgetter

RATINGS_DATA = '../data/ratings.csv'
ITEMS_DATA = '../data/movies.csv'
TAGS_DATA = '../data/tags.csv'

ratings_df = pd.read_csv(RATINGS_DATA)
movies_df = pd.read_csv(ITEMS_DATA)
tags_df = pd.read_csv(TAGS_DATA)

# Extract item features. Using One-Hot Encoding
# for representation.
movies_df.sort_values('movieId', inplace=True)

movie_index_map = movies_df['movieId'].to_dict()
movie_index_map_inv = {v: k for k, v in movie_index_map.items()}

def movie_map(ids: list, inv: int = 0):
    """Map each movie ID to its index on the dataframe and vice versa"""
    if inv:
        return list(itemgetter(*ids)(movie_index_map_inv))
    return list(itemgetter(*ids)(movie_index_map))

genres = movies_df[movies_df['genres'] != '(no genres listed)']['genres'].apply(lambda x: x.split('|')).explode().str.get_dummies().groupby(level=0).sum()

item_features = genres # TODO: Add tags and other features

# Example user ID for testing purposes.
test_user_id = 9
n_recommendations = 30

# Highest rated.
rated_items = ratings_df[ratings_df['userId'] == test_user_id][['movieId', 'rating']].sort_values('rating', ascending=False)
rated_items_index = movie_map(rated_items['movieId'].to_list(), inv = 1)

watched_list = movies_df.filter(items = rated_items_index, axis=0)[:n_recommendations]['title']

print(f"[+] User {test_user_id} have watched:")
print(watched_list)

# Item features of items rated by the user.
rated_items_features = item_features.filter(items = rated_items_index, axis = 0)

# Multiply each rated item features by its rating.
# The aggregate and normalize the features to get user profile.
weighted_genre_matrix = rated_items_features.mul(rated_items.sort_values('movieId')['rating'].to_list(), axis = 0) 
user_profile = weighted_genre_matrix.sum() / weighted_genre_matrix.sum().sum() # normalization

print("\n[+] User profile:")
print(user_profile.sort_values(ascending=False))

# Multiply user profile with the item features.
# Then aggregate the features of each item, items with
# the highest values will be recommended to the user.
weighted_movie_matrix = item_features.drop(index = rated_items_index).mul(user_profile.to_list())
recommendation_matrix = weighted_movie_matrix.sum(axis = 1)
recommendations_index = recommendation_matrix.sort_values(ascending=False).index
recommended_movies_ids = movie_map(recommendations_index.to_list())

print("\n[+] Recommended based on user's watch list :")
print(movies_df[movies_df['genres'] != '(no genres listed)'].filter(items = recommendations_index, axis=0)[:n_recommendations]['title'])

