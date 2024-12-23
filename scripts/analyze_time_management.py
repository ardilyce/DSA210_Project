import os
import pandas as pd
import matplotlib.pyplot as plt
import re


def load_processed_data(file_path):
    """
    Load the processed game data from a JSON file.
    """
    return pd.read_json(file_path)


def to_seconds(time_str):
    """
    Convert a time string in the format hours:minutes:seconds to seconds.
    """
    parts = list(map(float, time_str.split(":")))
    if len(parts) == 2:  # Format: mm:ss
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:  # Format: hh:mm:ss
        return parts[0] * 3600 + parts[1] * 60 + parts[2]


def extract_time_per_move(moves, player_color):
    """
    Extract and calculate the average time per move for a player (White or Black).
    """
    if player_color.lower() not in ["white", "black"]:
        raise ValueError("player_color must be 'white' or 'black'.")

    # Extract times based on the player's moves
    if player_color.lower() == "white":
        times = re.findall(r"[^\.]\.\s[^\[]+\[%clk\s([0-9:.]+)\]", moves)
    elif player_color.lower() == "black":
        times = re.findall(r"\.\.\.\s[^\[]+\[%clk\s([0-9:.]+)\]", moves)

    if len(times) <= 1:  # Not enough data to calculate time per move
        return None

    # Convert times into seconds
    times_in_seconds = list(map(to_seconds, times))

    # Calculate time differences (time per move)
    time_diffs = [
        times_in_seconds[i] - times_in_seconds[i + 1]
        for i in range(len(times_in_seconds) - 1)
        if times_in_seconds[i] > times_in_seconds[i + 1]  # Ignore anomalies
    ]
    return sum(time_diffs) / len(time_diffs) if time_diffs else None


def analyze_time_management(data, username):
    """
    Analyze time management for each time format and game outcome, focusing on the player's moves.
    """
    time_data = []

    for _, row in data.iterrows():
        if row["Time Class"].lower() == "daily":
            continue  # Exclude Daily games

        # Determine player's color
        player_color = "white" if row["White Player"].lower() == username.lower() else "black"
        
        # Extract average time per move for the player
        avg_time_per_move = extract_time_per_move(row["Moves"], player_color)

        if avg_time_per_move is not None:
            time_data.append({
                "Time Class": row["Time Class"],
                "Result": row["Result"],
                "Average Time Per Move": avg_time_per_move
            })

    # Convert to DataFrame
    time_data = pd.DataFrame(time_data)

    # Group by Time Class and Result
    grouped_data = time_data.groupby(["Time Class", "Result"]).agg({
        "Average Time Per Move": "mean"
    }).reset_index()

    return grouped_data


def plot_time_management(data, save_path):
    """
    Plot time management for all time formats in a single graph.
    """
    time_classes = data["Time Class"].unique()
    result_order = ["Loss", "Draw", "Win"]  # Desired order for results

    # Prepare data for plotting
    bar_width = 0.2
    x_positions = {time_class: i for i, time_class in enumerate(time_classes)}
    offset_map = {result: (idx - 1) * bar_width for idx, result in enumerate(result_order)}

    # Create plot
    plt.figure(figsize=(12, 6))
    for result in result_order:
        subset = data[data["Result"] == result]
        x_values = [x_positions[time_class] + offset_map[result] for time_class in subset["Time Class"]]
        y_values = subset["Average Time Per Move"]
        bars = plt.bar(
            x_values, y_values, bar_width, label=result,
            color="green" if result == "Win" else "red" if result == "Loss" else "blue"
        )

        # Annotate bars
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{bar.get_height():.2f} sec",
                ha="center",
                fontsize=10
            )

    # Configure plot aesthetics
    plt.xticks(
        [x_positions[time_class] for time_class in time_classes],
        time_classes, fontsize=12
    )
    plt.ylim(0, max(data["Average Time Per Move"]) * 1.1)  # Add some padding
    plt.title("Average Time Per Move by Game Outcome", fontsize=16)
    plt.xlabel("Time Format", fontsize=12)
    plt.ylabel("Average Time Per Move (seconds)", fontsize=12)
    plt.legend(title="Game Outcome", fontsize=10)
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

    # Analyze time management
    print("Analyzing time management...")
    time_management_stats = analyze_time_management(data, username)
    print("Time Management Statistics:")
    print(time_management_stats)

    # Save path for the plot
    time_management_plot_path = "./reports/figures/ardil30_time_management.png"

    # Plot and save time management statistics
    print("Plotting time management statistics...")
    plot_time_management(time_management_stats, time_management_plot_path)
    print("Analysis complete!")
