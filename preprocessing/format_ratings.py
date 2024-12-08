import pandas as pd

# Load the ratings.dat file with "::" as the delimiter
ratings_df = pd.read_csv('ratings.dat', delimiter='::', names=['user_id', 'movie_id', 'rating', 'timestamp'], engine='python')

# Sort by user_id, movie_id, and timestamp in descending order
ratings_df = ratings_df.sort_values(by=['user_id', 'movie_id', 'timestamp'], ascending=[True, True, False])

# Drop duplicates to keep the latest rating for each user_id and movie_id
ratings_df = ratings_df.drop_duplicates(subset=['user_id', 'movie_id'])

# Drop the timestamp column
ratings_df = ratings_df.drop(columns=['timestamp'])

# Save the result to ratings_dat.csv
ratings_df.to_csv('ratings_dat.csv', index=False)
print("Processed ratings data saved to 'ratings_dat.csv'.")
