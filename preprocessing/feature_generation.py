import pandas as pd

# Load the input CSV file
input_file = "merged_movie_data_flat.csv"
output_file = "merged_movie_data_flat_features.csv"
mappings_file = "mappings.txt"
df = pd.read_csv(input_file)

# Task 1: Drop the title column
df = df.drop(columns=['title'])

# Task 2: Extract unique values for specified columns
multi_valued_columns = {
    'genres': [f"genre{i}" for i in range(1, 9)],  # genre1 to genre8
    'production_companies': [f"production_company{i}" for i in range(1, 27)],  # production_company1 to production_company26
    'production_countries': [f"production_country{i}" for i in range(1, 13)],  # production_country1 to production_country12
    'spoken_languages': [f"spoken_language{i}" for i in range(1, 7)]  # spoken_language1 to spoken_language6
}
single_valued_columns = ['original_language']

# Initialize dictionaries to hold unique values
unique_values = {col: set() for col in multi_valued_columns.keys()}
unique_values.update({col: set() for col in single_valued_columns})

# Collect unique values for multi-valued columns
for col, columns in multi_valued_columns.items():
    for relevant_col in columns:
        unique_values[col].update(df[relevant_col].dropna().unique())

# Collect unique values for single-valued columns
for col in single_valued_columns:
    unique_values[col].update(df[col].dropna().unique())

# Task 3: Map unique values to integers (0 for empty values)
value_to_int = {}
int_to_value = {}

for col, unique_set in unique_values.items():
    value_map = {v: i + 1 for i, v in enumerate(sorted(unique_set))}
    value_map[''] = 0  # Handle empty values explicitly
    value_to_int[col] = value_map
    int_to_value[col] = {v: k for k, v in value_map.items()}  # Reverse mapping for debugging

# Task 4: Replace categorical values with numerical mappings
for col, columns in multi_valued_columns.items():
    for relevant_col in columns:
        df[relevant_col] = df[relevant_col].fillna('').map(value_to_int[col])

for col in single_valued_columns:
    df[col] = df[col].fillna('').map(value_to_int[col])

# Replace empty cells with 0
df = df.fillna(0)

# Save the transformed dataset to a new CSV file
df.to_csv(output_file, index=False)

# Write the mappings to a text file with UTF-8 encoding
with open(mappings_file, 'w', encoding='utf-8') as f:
    for col, value_map in value_to_int.items():
        f.write(f"{col} mapping:\n")
        for k, v in value_map.items():
            f.write(f"  {k}: {v}\n")
        f.write("\n")

print(f"Categorical values have been mapped to integers and saved to {output_file}.")
print(f"Mappings have been written to {mappings_file}.")
