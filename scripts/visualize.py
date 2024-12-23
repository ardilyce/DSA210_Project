import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Load the processed JSON data.
    """
    return pd.read_json(file_path)

def prepare_trend_data(data, username, window_size=20):
    """
    Prepare data for trend analysis by extracting relevant columns and applying smoothing.
    """
    # Convert end time to datetime
    data['End Time'] = pd.to_datetime(data['End Time'])

    # Add player rating column
    data['Player Rating'] = data.apply(
        lambda row: row['White Rating'] if row['White Player'] == username else row['Black Rating'], axis=1
    )

    # Add opponent rating column
    data['Opponent Rating'] = data.apply(
        lambda row: row['Black Rating'] if row['White Player'] == username else row['White Rating'], axis=1
    )

    # Sort by time
    data = data.sort_values('End Time')

    # Apply moving average to smooth ratings
    data['Smoothed Rating'] = data.groupby('Time Class')['Player Rating'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1).mean()
    )

    return data[['End Time', 'Time Class', 'Player Rating', 'Smoothed Rating', 'Opponent Rating']]

def plot_time_control(trend_data, time_class, save_path):
    """
    Plot smoothed rating trends for a specific time control and save the plot as an image.
    """
    subset = trend_data[trend_data['Time Class'] == time_class]

    # Debugging: Check if subset has data
    if subset.empty:
        print(f"No data found for time class: {time_class}")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(subset['End Time'], subset['Smoothed Rating'], label=f"{time_class.capitalize()} Rating", color='blue')
    plt.title(f"{time_class.capitalize()} Rating Trends Over Time (Smoothed)", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Rating", fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    # Save plot as an image
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, format="png")
    print(f"Plot saved to {save_path}")
    plt.close()

if __name__ == "__main__":
    username = "ardil30"  # Replace with your Chess.com username
    processed_data_path = f"./data/processed/{username}_games.json"

    # Paths for each time control's plot
    blitz_plot_path = f"./reports/figures/{username}_blitz_rating_trends.png"
    bullet_plot_path = f"./reports/figures/{username}_bullet_rating_trends.png"
    rapid_plot_path = f"./reports/figures/{username}_rapid_rating_trends.png"

    # Load processed data
    data = load_data(processed_data_path)

    # Debugging: Print loaded data
    print("Loaded Data (Sample):")
    print(data.head())

    # Prepare trend data with smoothing
    trend_data = prepare_trend_data(data, username)

    # Debugging: Print trend data
    print("Trend Data (Sample):")
    print(trend_data.head())

    # Plot and save rating trends for each time control
    plot_time_control(trend_data, "Blitz", blitz_plot_path)
    plot_time_control(trend_data, "Bullet", bullet_plot_path)
    plot_time_control(trend_data, "Rapid", rapid_plot_path)
