import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the JSON file
json_path = 'data/processed/ardil30_games.json'
data = pd.read_json(json_path)

# Ensure the 'End Time' column is in datetime format
data['End Time'] = pd.to_datetime(data['End Time'])

# Extract the month and categorize hours into time zones
data['month'] = data['End Time'].dt.month

def categorize_time(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Noon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

data['time_of_day'] = data['End Time'].dt.hour.apply(categorize_time)

# Group by month and time of day
games_by_time_of_day = data.groupby(['month', 'time_of_day']).size().reset_index(name='Game Count')

# Map time zones to shades of blue
color_map = {
    'Morning': '#add8e6',  # Light blue
    'Noon': '#6495ed',     # Cornflower blue
    'Evening': '#4169e1',  # Royal blue
    'Night': '#000080'     # Navy blue
}

# Plot the histogram
plt.figure(figsize=(12, 6))
for time_of_day, color in color_map.items():
    subset = games_by_time_of_day[games_by_time_of_day['time_of_day'] == time_of_day]
    plt.bar(subset['month'], subset['Game Count'], color=color, label=time_of_day, width=0.8)

# Add labels and legend
plt.xlabel('Month')
plt.ylabel('Number of Games Played')
plt.title('Games Played by Time of Day (Monthly)')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Time of Day')
plt.tight_layout()

# Ensure the directory exists
output_dir = 'reports/figures'
os.makedirs(output_dir, exist_ok=True)

# Save the plot as a PNG file
output_path = os.path.join(output_dir, 'games_by_time_of_day_shades.png')
plt.savefig(output_path)
plt.close()  # Close the plot to free up memory

print(f"Histogram saved to {output_path}")
