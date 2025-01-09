import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the JSON file
json_path = 'data/processed/ardil30_games.json'
data = pd.read_json(json_path)

# Ensure the 'End Time' column is in datetime format
data['End Time'] = pd.to_datetime(data['End Time'])

# Extract the day of the week
data['day_of_week'] = data['End Time'].dt.day_name()

# Categorize results into win, loss, or draw
def map_result_to_category(result):
    if 'Win' in result:
        return 'Win'
    elif 'Loss' in result:
        return 'Loss'
    elif 'Draw' in result:
        return 'Draw'
    else:
        return 'Other'

data['Result Category'] = data['Result'].apply(map_result_to_category)

# Group data by day of the week and result category
result_by_day = data.groupby(['day_of_week', 'Result Category']).size().unstack(fill_value=0)

# Reorder the days of the week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
result_by_day = result_by_day.reindex(day_order)

# Define color shades
color_map = {
    'Win': '#98fb98',   # Pale green
    'Draw': '#a9a9a9',  # Dark gray
    'Loss': '#ff7f7f'   # Light red
}

# Plot the stacked bar chart
result_by_day[['Win', 'Draw', 'Loss']].plot(
    kind='bar',
    stacked=True,
    figsize=(12, 6),
    color=[color_map['Win'], color_map['Draw'], color_map['Loss']]
)

# Add title and labels
plt.title('Number of Games Played by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Games Played')
plt.xticks(rotation=45)
plt.legend(title='Result')
plt.tight_layout()

# Ensure the directory exists
output_dir = 'reports/figures'
os.makedirs(output_dir, exist_ok=True)

# Save the plot as a PNG file
output_path = os.path.join(output_dir, 'games_by_day_results.png')
plt.savefig(output_path)
plt.close()  # Close the plot to free up memory

print(f"Stacked bar chart saved to {output_path}")
