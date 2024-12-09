import pandas as pd

# 1. Drop the 'zip_code' column from users_dat_filter.csv and create users_refined_A.csv
users_df = pd.read_csv('users_dat_filter.csv')

# Drop the 'zip_code' column
users_df.drop(columns=['zip_code'], inplace=True)

# Save the refined users data to a new file
users_df.to_csv('users_refined_A.csv', index=False)
print("users_refined_A.csv has been created with the zip_code column removed.")

# 2. Filter ratings that have a movie_id present in merged_movie_data_flat_features.csv
ratings_df = pd.read_csv('ratings_dat_filter.csv')

# Load the merged_movie_data_flat_features.csv to get the valid movie_ids
merged_movie_data_df = pd.read_csv('merged_movie_data_flat_features.csv')

# Get the valid movie_ids from the merged file
valid_movie_ids = merged_movie_data_df['movie_id'].unique()

# Filter the ratings based on valid movie_ids
filtered_ratings_df = ratings_df[ratings_df['movie_id'].isin(valid_movie_ids)]

# Save the filtered ratings to a new file
filtered_ratings_df.to_csv('ratings_refined.csv', index=False)
print("ratings_refined.csv has been created with filtered ratings based on valid movie_ids.")
