import pandas as pd

# Load the movies_dat.csv and metadata_filter_flat.csv files
movies_df = pd.read_csv('movies_dat.csv')
metadata_df = pd.read_csv('metadata_filter_flat.csv')

# Filter movies_df to retain only those movies whose title is in the metadata_df title column
filtered_movies_df = movies_df[movies_df['movie_title'].isin(metadata_df['title'])]

# Save the filtered result to a new file
filtered_movies_df.to_csv('filtered_movies.csv', index=False)
print(f"Filtered movies saved to 'filtered_movies.csv'.")
