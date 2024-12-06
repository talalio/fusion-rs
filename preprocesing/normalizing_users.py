import pandas as pd

# Load the users.dat file with "::" as the delimiter
users_df = pd.read_csv('users.dat', delimiter='::', names=['user_id', 'gender', 'age', 'occupation', 'zip_code'], engine='python')

# Save the cleaned data to users_dat.csv
users_df.to_csv('users_dat.csv', index=False)
print("Processed users data saved to 'users_dat.csv'.")
