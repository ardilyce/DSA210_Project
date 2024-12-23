import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

def load_data(file_path):
    """
    Load processed game data from JSON file.
    """
    return pd.read_json(file_path)

def add_player_rating(data, username):
    """
    Add 'Player Rating' column to the dataset based on the user's color.
    """
    print("Adding 'Player Rating' to the dataset...")
    data["Player Rating"] = data.apply(
        lambda row: row["White Rating"] if row["White Player"] == username else row["Black Rating"],
        axis=1
    )
    return data

def calculate_opening_effectiveness(data):
    """
    Calculate win, draw, and loss rates for each opening.
    """
    print("Calculating opening effectiveness...")
    opening_stats = data.groupby("Main Opening").apply(
        lambda x: pd.Series({
            "Games Played": len(x),
            "Win Rate (%)": (x["Result"] == "Win").mean() * 100,
            "Draw Rate (%)": (x["Result"] == "Draw").mean() * 100,
            "Loss Rate (%)": (x["Result"] == "Loss").mean() * 100
        })
    )
    return opening_stats.sort_values(by="Games Played", ascending=False)

def plot_top_openings(opening_stats, top_n=10, save_path="./reports/figures/opening_effectiveness_bar_chart.png"):
    """
    Plot the win/draw/loss rates for the top N most-played openings.
    """
    top_openings = opening_stats.head(top_n)
    print(f"Top {top_n} openings:\n", top_openings)

    # Create a stacked bar chart
    top_openings[["Win Rate (%)", "Draw Rate (%)", "Loss Rate (%)"]].plot(
        kind="bar", stacked=True, figsize=(12, 6), color=["green", "blue", "red"]
    )
    plt.title(f"Top {top_n} Openings by Win/Draw/Loss Rates")
    plt.xlabel("Main Opening")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Outcome")
    plt.tight_layout()

    # Save the plot
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Opening effectiveness chart saved to {save_path}")
    plt.close()

def save_opening_statistics(opening_stats, save_path="./reports/data/opening_effectiveness.csv"):
    """
    Save opening statistics to a CSV file for further analysis.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    opening_stats.to_csv(save_path)
    print(f"Opening effectiveness data saved to {save_path}")

if __name__ == "__main__":
    # Paths
    data_path = "./data/processed/ardil30_games.json"
    chart_path = "./reports/figures/opening_effectiveness_bar_chart.png"
    stats_path = "./reports/data/opening_effectiveness.csv"
    username = "your_username"  # Replace with your Chess.com username

    # Load data
    print("Loading data...")
    data = load_data(data_path)

    # Add Player Rating
    data = add_player_rating(data, username)

    # Split the data into training (80%) and testing (20%) sets
    print("Splitting data...")
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    # Calculate opening effectiveness using the training data
    opening_stats = calculate_opening_effectiveness(train_data)

    # Save the results
    save_opening_statistics(opening_stats, save_path=stats_path)

    # Plot the top openings
    plot_top_openings(opening_stats, top_n=10, save_path=chart_path)
