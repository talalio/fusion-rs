import pandas as pd

# Load the ratings and merged movie data files
ratings_df = pd.read_csv('ratings_dat.csv')
merged_movies_df = pd.read_csv('merged_movie_data.csv')

# Filter ratings where movie_id exists in merged_movie_data.csv
filtered_ratings_df = ratings_df[ratings_df['movie_id'].isin(merged_movies_df['movie_id'])]

# Save the filtered ratings to a new CSV file
filtered_ratings_df.to_csv('ratings_dat_filter.csv', index=False)

print("Filtered ratings saved to 'ratings_dat_filter.csv'.")
