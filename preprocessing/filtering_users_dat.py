import pandas as pd

# Load the users and filtered ratings data
users_df = pd.read_csv('users_dat.csv')
filtered_ratings_df = pd.read_csv('ratings_dat_filter.csv')

# Filter users where user_id exists in ratings_dat_filter.csv
filtered_users_df = users_df[users_df['user_id'].isin(filtered_ratings_df['user_id'])]

# Save the filtered users to a new CSV file
filtered_users_df.to_csv('users_dat_filter.csv', index=False)

print("Filtered users saved to 'users_dat_filter.csv'.")
