import pandas as pd


'''
Post-process data
'''

# Load the CSV file
df = pd.read_csv('IFEWs.csv')

# Display the count of missing values per column to understand the data better
# Drop rows where 'Number' has NaN values
df_cleaned = df.dropna(subset=['Number'])

# Remove rows where 'Number' starts with a dash ('-')
df_cleaned = df_cleaned[~df_cleaned['Number'].astype(str).str.startswith('-')]

# Convert 'Number' to numeric, forcing errors to NaN (in case some values can't be converted)
df_cleaned['Number'] = pd.to_numeric(df_cleaned['Number'], errors='coerce')

# Drop rows with NaN in 'Number' after conversion (these were non-numeric values)
df_cleaned = df_cleaned.dropna(subset=['Number'])

# Filter out rows where 'Number' is greater than 400,000
df_cleaned = df_cleaned[df_cleaned['Number'] <= 6000]
# Save the cleaned DataFrame to a new CSV file
df_cleaned.to_csv('IFEWs.csv', index=False)


