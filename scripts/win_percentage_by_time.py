import pandas as pd

# Load the JSON file
json_path = 'data/processed/ardil30_games.json'
data = pd.read_json(json_path)

# Ensure the 'End Time' column is in datetime format
data['End Time'] = pd.to_datetime(data['End Time'])

# Extract the hour from 'End Time'
data['hour'] = data['End Time'].dt.hour

# Categorize hours into time zones
def categorize_time(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Noon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

data['time_of_day'] = data['hour'].apply(categorize_time)

# Determine if the game was a win
data['is_win'] = data['Result'].str.contains('Win', case=False)

# Group by time of day and calculate win rate and match count
stats_by_time_of_day = data.groupby('time_of_day').agg(
    matches_played=('is_win', 'size'),
    win_rate=('is_win', 'mean')
).reset_index()

# Define the custom sort order
time_of_day_order = ['Morning', 'Noon', 'Evening', 'Night']
stats_by_time_of_day['time_of_day'] = pd.Categorical(
    stats_by_time_of_day['time_of_day'], 
    categories=time_of_day_order, 
    ordered=True
)

# Sort the DataFrame
stats_by_time_of_day = stats_by_time_of_day.sort_values('time_of_day')

# Print the results
print("Performance by Time of Day:")
for _, row in stats_by_time_of_day.iterrows():
    print(f"{row['time_of_day']}: Matches Played: {row['matches_played']}, Win Rate: {row['win_rate']:.2%}")
