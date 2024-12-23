import os
import pandas as pd
import matplotlib.pyplot as plt

def load_processed_data(file_path):
    """
    Load the processed game data from a JSON file.
    """
    return pd.read_json(file_path)

def calculate_rating_differential(row, username):
    """
    Calculate rating differential for the player (opponent_rating - my_rating).
    """
    player_rating = (
        row["White Rating"] if row["White Player"].lower() == username.lower()
        else row["Black Rating"]
    )
    opponent_rating = (
        row["Black Rating"] if row["White Player"].lower() == username.lower()
        else row["White Rating"]
    )
    return opponent_rating - player_rating

def group_by_rating_differential(data, username):
    """
    Group games by smaller rating differentials (10-point intervals) and calculate win rates.
    """
    # Calculate rating differential for each game
    data["Rating Differential"] = data.apply(
        lambda row: calculate_rating_differential(row, username), axis=1
    )

    # Define rating differential bins
    bins = [-float("inf")] + list(range(-70, 71, 10)) + [float("inf")]
    labels = [f"{bins[i]} to {bins[i+1]}" for i in range(len(bins) - 1)]

    # Categorize each game into a bin
    data["Rating Differential Bin"] = pd.cut(
        data["Rating Differential"], bins=bins, labels=labels, right=False
    )

    # Calculate win rate for each bin
    differential_stats = data.groupby("Rating Differential Bin").apply(
        lambda x: pd.Series({
            "Games Played": len(x),
            "Win Rate": (x["Result"] == "Win").mean() * 100
        })
    )

    return differential_stats

def plot_stats(stats, title, xlabel, ylabel, save_path):
    """
    Plot win rates based on calculated stats.
    """
    plt.figure(figsize=(12, 6))
    bars = plt.bar(stats.index.astype(str), stats["Win Rate"], color="blue")

    # Annotate each bar with the number of games played
    for bar, games in zip(bars, stats["Games Played"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{int(games)} games",
            ha="center",
            fontsize=10
        )

    # Add a note to the graph
    plt.figtext(
        0.99, 0.01, 
        "Rating Differential = Opponent Rating - My Rating", 
        horizontalalignment="right", fontsize=10, color="gray"
    )

    # Set chart limits and labels
    plt.ylim(0, 100)  # Y-axis from 0 to 100%
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
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

    # Group games by rating differential and calculate win rates
    print("Grouping games by rating differential...")
    differential_stats = group_by_rating_differential(data, username)

    # Print stats to console
    print("Win Rate by Rating Differential:")
    print(differential_stats)

    # Save path for the plot
    differential_plot_path = "./reports/figures/ardil30_rating_differential_stats.png"

    # Plot and save rating differential statistics
    print("Plotting rating differential statistics...")
    plot_stats(
        differential_stats,
        "Win Rate by Rating Differential",
        "Rating Differential",
        "Win Rate (%)",
        differential_plot_path
    )
    print("Analysis complete!")
