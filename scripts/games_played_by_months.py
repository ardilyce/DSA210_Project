import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the JSON file
json_path = 'data/processed/ardil30_games.json'
data = pd.read_json(json_path)

# Ensure the 'End Time' column is in datetime format
data['End Time'] = pd.to_datetime(data['End Time'])

# Extract year and month
data['year_month'] = data['End Time'].dt.to_period('M')

# Count the number of games per year-month
games_by_month = data['year_month'].value_counts().sort_index()

# Convert to DataFrame for better handling
games_by_month_df = games_by_month.reset_index()
games_by_month_df.columns = ['Year-Month', 'Game Count']

# Plot the histogram
plt.figure(figsize=(12, 6))
plt.bar(games_by_month_df['Year-Month'].astype(str), games_by_month_df['Game Count'], width=0.8)
plt.xticks(rotation=45)
plt.xlabel('Year-Month')
plt.ylabel('Number of Games Played')
plt.title('Number of Games Played by Month')
plt.tight_layout()

# Ensure the directory exists
output_dir = 'reports/figures'
os.makedirs(output_dir, exist_ok=True)

# Save the plot to the reports/figures directory
output_path = os.path.join(output_dir, 'games_by_month_histogram.png')
plt.savefig(output_path)
plt.close()  # Close the plot to free up memory

print(f"Histogram saved to {output_path}")
