import pandas as pd

# Load the CSV files
dataset_df = pd.read_csv('dataset_filter.csv', low_memory=False)
tmdb_df = pd.read_csv('tmdb_filter.csv', low_memory=False)

# 1. Compare Columns in Both Files
columns_in_dataset = set(dataset_df.columns)
columns_in_tmdb = set(tmdb_df.columns)

# Attributes in dataset_filter.csv but not in tmdb_filter.csv
dataset_not_in_tmdb = columns_in_dataset - columns_in_tmdb
# Attributes in tmdb_filter.csv but not in dataset_filter.csv
tmdb_not_in_dataset = columns_in_tmdb - columns_in_dataset

print(f"Attributes in dataset_filter.csv but not in tmdb_filter.csv: {dataset_not_in_tmdb}")
print(f"Attributes in tmdb_filter.csv but not in dataset_filter.csv: {tmdb_not_in_dataset}")

# 2. Total Number of Rows in Both Files
dataset_row_count = len(dataset_df)
tmdb_row_count = len(tmdb_df)

print(f"Total rows in dataset_filter.csv: {dataset_row_count}")
print(f"Total rows in tmdb_filter.csv: {tmdb_row_count}")

# 3. Extract the first and last 50 rows from both files
first_50_tmdb = tmdb_df.head(50)['title']
last_50_tmdb = tmdb_df.tail(50)['title']
first_50_dataset = dataset_df.head(50)['title']
last_50_dataset = dataset_df.tail(50)['title']

# 4. Compare the 'title' attribute for first 50 and last 50 rows

def compare_rows_title(df1, df2, row_range):
    """Compare the 'title' column values for the specified row range."""
    return df1.iloc[row_range].equals(df2.iloc[row_range])

# Compare first 50 rows
first_50_match = compare_rows_title(first_50_dataset, first_50_tmdb, slice(0, 50))
print(f"First 50 rows match for 'title' column: {first_50_match}")

# Compare last 50 rows
last_50_match = compare_rows_title(last_50_dataset, last_50_tmdb, slice(0, 50))
print(f"Last 50 rows match for 'title' column: {last_50_match}")

'''
OUTPUT:
Attributes in dataset_filter.csv but not in tmdb_filter.csv: {'crew', 'index', 'cast', 'director'}
Attributes in tmdb_filter.csv but not in dataset_filter.csv: set()
Total rows in dataset_filter.csv: 863
Total rows in tmdb_filter.csv: 863
First 50 rows match for 'title' column: True
Last 50 rows match for 'title' column: True
'''