import pandas as pd

# Load users_refined_A.csv
users_refined_df = pd.read_csv('users_refined_A.csv')

# Load ratings_refined.csv
ratings_refined_df = pd.read_csv('ratings_refined.csv')

# Get the set of user_ids that appear in ratings_refined.csv
valid_user_ids = ratings_refined_df['user_id'].unique()

# Filter out users who are not in ratings_refined.csv
filtered_users_df = users_refined_df[users_refined_df['user_id'].isin(valid_user_ids)]

# Map 'M' to 1, 'F' to 2, and NaN/missing values to 0 using apply()
filtered_users_df['gender'] = filtered_users_df['gender'].apply(lambda x: 1 if x == 'M' else (2 if x == 'F' else 0))

# Save the filtered users data with the modified gender column to a new file
filtered_users_df.to_csv('users_refined_B.csv', index=False)
print("users_refined_B.csv has been created with users who have at least one rating and the gender column modified.")
