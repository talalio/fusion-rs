import pandas as pd

# Load the filtered movies file and metadata_filter_flat.csv
filtered_movies_df = pd.read_csv('filtered_movies.csv')
metadata_df = pd.read_csv('metadata_filter_flat.csv')

# Initialize an empty list to store merged movie data
merged_data = []

# Loop over the filtered movies and merge the genres
for _, row in filtered_movies_df.iterrows():
    movie_title = row['movie_title']
    movie_genres = row['genres'].split('|')  # Split genres by '|'
    
    # Find the corresponding metadata row
    metadata_row = metadata_df[metadata_df['title'] == movie_title].iloc[0]
    
    # Get genres from metadata, and handle the case if genres is NaN or empty
    metadata_genres = metadata_row['genres']
    
    if isinstance(metadata_genres, str):  # Only split if it's a string
        metadata_genres = metadata_genres.split('-')
    else:
        metadata_genres = []  # If genres is missing or NaN, use an empty list
    
    # Combine genres from both sources, remove duplicates, and join them back into a dash-separated string
    combined_genres = list(set(movie_genres + metadata_genres))
    combined_genres_str = '-'.join(sorted(combined_genres))
    
    # Create the new row for the merged dataset
    merged_row = {
        'movie_id': row['movie_id'],
        'title': metadata_row['title'],
        'release_year': row['release_year'],
        'genres': combined_genres_str,
    }
    
    # Add the rest of the attributes from the metadata file
    for column in metadata_df.columns:
        if column not in merged_row:  # Avoid duplicate columns
            merged_row[column] = metadata_row[column]
    
    # Append the merged row to the merged_data list
    merged_data.append(merged_row)

# Create a DataFrame from the merged data
merged_df = pd.DataFrame(merged_data)

# Save the merged data to a new CSV file
merged_df.to_csv('merged_movie_data.csv', index=False)
print(f"Merged movie data saved to 'merged_movie_data.csv'.")
