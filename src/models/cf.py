import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from scipy.sparse import csr_matrix


class CF():

    def __init__(self, ratings_data_path, movies_data_path):
        self.ratings = pd.read_csv(ratings_data_path)
        self.movies = pd.read_csv(movies_data_path)
        self.item_factors = None
        self.user_factors = None

    def recommend(self, movie_title, top_n=5):
        utility_matrix, movie_mapper, movie_inv_mapper = self._create_sparse_matrix(self.ratings)
        _, i_factors = self._apply_nmf(utility_matrix)

        movie_similarity = self._get_cosine_similarity(i_factors)
        movie_id = self.get_movie_id(movie_title)

        if movie_id not in movie_mapper:
            raise ValueError("Movie ID not found in matrix.")

        movie_index = movie_mapper[movie_id]

        similarity_scores = list(enumerate(movie_similarity[movie_index]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True) # Descending (highest to lowest)

        # Filter out the matched movie's own index
        recommended_movie_indices = [i[0] for i in sorted_scores if i[0] != movie_index][:top_n]
        recommended_movie_ids = [movie_inv_mapper[idx] for idx in recommended_movie_indices]

        recommended_movies = self.movies[self.movies['movieId'].isin(recommended_movie_ids)]['title'].tolist()
        return recommended_movies
        
    def _create_sparse_matrix(self, df: pd.DataFrame):
        U = df['userId'].nunique() # number of unique users
        M = df['movieId'].nunique() # number of unique movies

        # create a user and movie id mapper dictionary
        # {user_id: user_index} => e.g. {0: 1}
        user_mapper = dict(zip(np.unique(df['userId']), list(range(U))))
        movie_mapper = dict(zip(np.unique(df['movieId']), list(range(M))))

        movie_inv_mapper = dict(zip(list(range(M)), np.unique(df['movieId'])))

        # exteract unique user and movie ids
        user_index = [user_mapper[i] for i in df['userId']]
        item_index = [movie_mapper[i] for i in df['movieId']]

        X = csr_matrix((df['rating'], (user_index, item_index)), shape=(U,M))

        return X, movie_mapper, movie_inv_mapper

    def _get_cosine_similarity(self, factors):
        return cosine_similarity(factors.T)

    def _get_sparsity(self, matrix):
        return (matrix.nnz / (matrix.shape[0] * matrix.shape[1]))

    def get_movie_id(self, title):
        choices = self.movies['title'].tolist()
        closest_match = process.extractOne(title, choices)
        if closest_match:
            match_title = closest_match[0]
            movie_id = self.movies[self.movies['title'] == match_title]['movieId'].values[0]
            # print(f"Matched input to: '{match_title}' (Movie ID: {movie_id})") # debug
            return movie_id
        else:
            # raise ValueError("No close match found for the movie title.")
            return None

    def _apply_nmf(self, u_matrix):
        # Apply Non-negative Matrix Factorization (NMF)
        nmf = NMF(n_components=30, max_iter=160, random_state=42)
        user_factors = nmf.fit_transform(u_matrix)
        item_factors = nmf.components_
        return (user_factors, item_factors)
