import pandas as pd

# File path to companies.csv
COMPANIES_FILE = "data/salesforce/companies.csv"

# Load the CSV file
companies_df = pd.read_csv(COMPANIES_FILE)

# Add the 'last_modified_date' column and set it to the value of 'created_date'
companies_df['last_modified_date'] = companies_df['created_date']

# Save the updated CSV file
companies_df.to_csv(COMPANIES_FILE, index=False)

print(f"'last_modified_date' column added to {COMPANIES_FILE}")
