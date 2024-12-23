import os
import pandas as pd
import matplotlib.pyplot as plt

def load_processed_data(file_path):
    """
    Load the processed game data from a JSON file.
    """
    return pd.read_json(file_path)

def analyze_openings(data):
    """
    Analyze most frequent main openings and their win rates.
    """
    # Calculate win rate for each main opening
    opening_stats = data.groupby('Main Opening').apply(
        lambda x: pd.Series({
            'Games Played': len(x),
            'Win Rate': (x['Result'] == 'Win').mean() * 100
        })
    )

    # Filter openings with at least 10 games
    opening_stats = opening_stats[opening_stats['Games Played'] >= 10]

    # Sort by the number of games played
    opening_stats = opening_stats.sort_values(by='Games Played', ascending=False)
    return opening_stats

def plot_opening_stats(opening_stats, save_path):
    """
    Plot the most common main openings and their win rates.
    """
    top_openings = opening_stats.head(10)  # Top 10 most played openings
    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_openings.index, top_openings['Win Rate'], color='blue')

    # Annotate each bar with the number of games played
    for bar, games in zip(bars, top_openings['Games Played']):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{int(games)} games",
            ha='center',
            fontsize=10
        )

    # Set chart limits and labels
    plt.ylim(0, 100)  # Y-axis from 0 to 100%
    plt.title("Top 10 Main Openings by Win Rate", fontsize=16)
    plt.xlabel("Main Opening", fontsize=12)
    plt.ylabel("Win Rate (%)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save plot
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, format="png")
    print(f"Plot saved to {save_path}")
    plt.close()

if __name__ == "__main__":
    # File path for processed data
    processed_data_path = "./data/processed/ardil30_games.json"
    username = "ardil30"  # Replace with your Chess.com username

    # Load processed data
    print("Loading processed game data...")
    data = load_processed_data(processed_data_path)

    # Analyze main openings
    print("Analyzing main openings...")
    opening_stats = analyze_openings(data)
    print("Main Opening Statistics (Top 10):")
    print(opening_stats.head(10))

    # Save path for the plot
    opening_plot_path = "./reports/figures/ardil30_main_opening_stats.png"

    # Plot and save main opening statistics
    print("Plotting main opening statistics...")
    plot_opening_stats(opening_stats, opening_plot_path)
    print("Analysis complete!")
