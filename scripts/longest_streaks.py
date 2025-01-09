import pandas as pd

# Load the JSON file
json_path = 'data/processed/ardil30_games.json'
data = pd.read_json(json_path)

# Ensure the 'Result' column exists
if 'Result' not in data.columns:
    raise ValueError("The 'Result' column is missing from the dataset.")

# Map results to streak types
def map_result_to_streak(result):
    if 'Win' in result:
        return 'Win'
    elif 'Loss' in result:
        return 'Loss'
    elif 'Draw' in result:
        return 'Draw'
    else:
        return None

data['streak_type'] = data['Result'].apply(map_result_to_streak)

# Ensure streaks are sorted by game order (assuming games are in chronological order)
# If not, sort by 'End Time' or relevant time column
data = data.sort_values('End Time')

# Calculate streaks
longest_streaks = {'Win': 0, 'Loss': 0, 'Draw': 0}
current_streak = {'type': None, 'count': 0}

for streak in data['streak_type']:
    if streak == current_streak['type']:
        current_streak['count'] += 1
    else:
        if current_streak['type']:
            longest_streaks[current_streak['type']] = max(
                longest_streaks[current_streak['type']],
                current_streak['count']
            )
        current_streak['type'] = streak
        current_streak['count'] = 1

# Handle the final streak
if current_streak['type']:
    longest_streaks[current_streak['type']] = max(
        longest_streaks[current_streak['type']],
        current_streak['count']
    )

# Print the results
print("Longest Streaks:")
for streak_type, streak_length in longest_streaks.items():
    print(f"{streak_type}: {streak_length}")
