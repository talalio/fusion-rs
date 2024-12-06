import pandas as pd

# Read the movie titles from movies_dat.csv
movies_dat_df = pd.read_csv('movies_dat.csv')

# Extract the movie titles from movies_dat.csv
movie_titles_set = set(movies_dat_df['movie_title'].str.strip())

# Helper function to filter a CSV file based on matching movie titles
def filter_movie_titles(input_file, output_file, title_column_name):
    # Read the CSV with low_memory=False to avoid dtype warning
    df = pd.read_csv(input_file, low_memory=False)
    
    # Filter rows where the title matches
    filtered_df = df[df[title_column_name].str.strip().isin(movie_titles_set)]
    
    # Save the filtered data to a new file
    filtered_df.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

# Filter each of the four files
filter_movie_titles('imdb_top_1000.csv', 'imdb_filter.csv', 'Series_Title')
filter_movie_titles('tmdb_5000_movies.csv', 'tmdb_filter.csv', 'title')
filter_movie_titles('movie_dataset.csv', 'dataset_filter.csv', 'title')
filter_movie_titles('movies_metadata.csv', 'metadata_filter.csv', 'title')
