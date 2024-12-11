import pandas as pd

# Read the CSV file
input_file = "C:\Users\arika\Downloads\Foreign-Born Population.zip\Foreign-Born Population" # Replace with your CSV file name
output_file = 'Utah_Foreign_Born.csv'  # The name of the output file

# Load the CSV into a DataFrame
df = pd.read_csv(input_file)

# Split the city column into city name and state abbreviation
df[['city_name', 'state_abbr']] = df['city'].str.rsplit(', ', n=1, expand=True)

# Filter for rows where the state abbreviation is UT
utah_only = df[df['state_abbr'] == 'UT']

# Drop the temporary columns (city_name and state_abbr) if not needed
utah_only = utah_only.drop(columns=['city_name', 'state_abbr'])

# Save the filtered DataFrame to a new CSV file
utah_only.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
