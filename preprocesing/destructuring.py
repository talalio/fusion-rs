import pandas as pd
import ast

# Load the metadata_filter.csv file
input_file = "metadata_filter.csv"
output_file = "processed_metadata_filter.csv"

# Define columns to drop
columns_to_drop = [
    "adult", "belongs_to_collection", "homepage", "id", "imdb_id", 
    "overview", "popularity", "status", "tagline", "video", "vote_count"
]

# Function to process JSON-like columns
def process_json_column(value, column_name):
    try:
        # Safely evaluate the string to a Python list/dict
        items = ast.literal_eval(value)
        
        # If the column is 'spoken_languages', we only need the 'name' property for the language
        if column_name == "spoken_languages":
            # Assuming the structure is a list of dictionaries with 'name' for the language
            if isinstance(items, list) and items:
                return '-'.join(item['name'] for item in items if 'name' in item)
        else:
            # For other columns (e.g., 'genres', 'production_companies', 'production_countries')
            if isinstance(items, list):
                return '-'.join(item['name'] for item in items if 'name' in item)
    except (ValueError, SyntaxError):
        pass
    return ""

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Drop specified columns
df = df.drop(columns=columns_to_drop)

# Process the JSON-like columns
columns_to_process = ["genres", "production_companies", "production_countries", "spoken_languages"]

for column in columns_to_process:
    df[column] = df[column].apply(process_json_column, column_name=column)

# Save the processed DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
