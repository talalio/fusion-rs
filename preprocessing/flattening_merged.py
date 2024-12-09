import pandas as pd

# Load the CSV file
input_file = "merged_movie_data.csv"
output_file = "merged_movie_data_flat.csv"
df = pd.read_csv(input_file)

# Task 1: Identify the max number of caret-separated values
split_columns = ['genres', 'production_companies', 'production_countries', 'spoken_languages']
max_lengths = {}
max_records = {}

for column in split_columns:
    if column in df.columns:
        # Ensure all values are strings before splitting
        df[column] = df[column].fillna('').astype(str)
        
        # Compute the max number of caret-separated values and the corresponding row index
        df[column + '_count'] = df[column].apply(lambda x: len(x.split('^')))
        max_lengths[column] = df[column + '_count'].max()
        max_index = df[column + '_count'].idxmax()
        
        # Store the title and count for the max record
        max_records[column] = {
            'title': df.loc[max_index, 'title'],
            'count': max_lengths[column]
        }

# Task 2: Save max values into variables
genresN = max_lengths['genres']
companiesN = max_lengths['production_companies']
countriesN = max_lengths['production_countries']
languagesN = max_lengths['spoken_languages']

# Task 3: Print the results
print(f"Max number of genres: {genresN} (Movie: {max_records['genres']['title']})")
print(f"Max number of production companies: {companiesN} (Movie: {max_records['production_companies']['title']})")
print(f"Max number of production countries: {countriesN} (Movie: {max_records['production_countries']['title']})")
print(f"Max number of spoken languages: {languagesN} (Movie: {max_records['spoken_languages']['title']})")

# Task 4: Flatten the multi-valued columns
for column, max_n in zip(split_columns, [genresN, companiesN, countriesN, languagesN]):
    # Split the values and create new columns
    new_columns = [f"{column[:-1]}{i+1}" for i in range(max_n)]  # e.g., genre1, genre2, ...
    df[new_columns] = df[column].apply(lambda x: pd.Series(x.split('^')))

# Drop the original multi-valued columns and helper count columns
df = df.drop(columns=split_columns + [col + '_count' for col in split_columns])

# Save to a new CSV file
df.to_csv(output_file, index=False)
print(f"Flattened data saved to {output_file}")