import os
import json
import pandas as pd
from datetime import datetime

def load_openings(file_path):
    """
    Load a list of main openings from a text file.
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            pass  # Create an empty file

    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def add_opening_to_file(file_path, opening):
    """
    Add a new opening to the openings file if it doesn't already exist.
    """
    openings = load_openings(file_path)
    if opening not in openings:
        with open(file_path, "a") as file:
            file.write(opening + "\n")
        print(f"New opening added to {file_path}: {opening}")

def split_pgn(pgn):
    """
    Split PGN into metadata (headers) and move list.
    Format the metadata as a dictionary for better readability.
    """
    if not pgn:
        return {"Information": {}, "Moves": "No Moves available"}

    try:
        parts = pgn.split("\n\n")  # Split PGN into headers and moves
        metadata_lines = parts[0].strip().split("\n")  # Split headers by lines
        moves = parts[1].strip() if len(parts) > 1 else "No Moves available"  # Moves section

        # Convert metadata lines to a dictionary
        metadata = {}
        for line in metadata_lines:
            if line.startswith("[") and line.endswith("]"):
                key_value = line[1:-1].split(" ", 1)  # Remove brackets and split by the first space
                if len(key_value) == 2:
                    key, value = key_value
                    metadata[key] = value.strip('"')  # Remove quotes around values

        return {"Information": metadata, "Moves": moves}
    except IndexError:
        return {"Information": {}, "Moves": "Invalid PGN format"}

def determine_game_result(game, username):
    """
    Determine the result of the game for the given player.
    """
    white_player = game.get("white", {}).get("username", "").lower()
    black_player = game.get("black", {}).get("username", "").lower()
    white_result = game.get("white", {}).get("result", "").lower()
    black_result = game.get("black", {}).get("result", "").lower()

    if username.lower() == white_player.strip().lower():
        if white_result == "win":
            return "Win"
        elif white_result in ["checkmated", "timeout", "resigned", "abandoned"]:
            return "Loss"
        elif white_result in ["stalemate", "draw", "insufficient material", "insufficient", "repetition", "agreed", "50move", "timevsinsufficient"]:
            return "Draw"
    elif username.lower() == black_player.strip().lower():
        if black_result == "win":
            return "Win"
        elif black_result in ["checkmated", "timeout", "resigned", "abandoned"]:
            return "Loss"
        elif black_result in ["stalemate", "draw", "insufficient material", "insufficient", "repetition", "agreed", "50move", "timevsinsufficient"]:
            return "Draw"
    return "Unknown"

def process_game_data(all_games, username, openings_file):
    """
    Beautify and structure game data with main openings and variations.
    """
    def unix_to_readable(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

    # Load main openings from the text file
    main_openings = load_openings(openings_file)

    game_list = []
    for game in all_games:
        pgn_split = split_pgn(game.get("pgn", ""))

        # Extract opening name
        opening_name = game.get("eco", "Unknown").split("/")[-1].replace("-", " ").capitalize()

        # Determine game result
        game_result = determine_game_result(game, username)

        # Determine main opening and variation
        main_opening = "Unknown"
        variation = opening_name

        for main in main_openings:
            if opening_name.lower().find(main.lower()) != -1:
                main_opening = main
                variation = opening_name.strip().capitalize()
                break

        # Add unknown opening to the openings file
        if main_opening == "Unknown" and opening_name != "Unknown":
            add_opening_to_file(openings_file, opening_name)
            main_opening = opening_name
            variation = "Unknown"

        game_entry = {
            "Game URL": game.get("url", ""),
            "Time Class": game.get("time_class", "N/A").capitalize(),
            "End Time": unix_to_readable(game.get("end_time", 0)),
            "White Player": game.get("white", {}).get("username", "Unknown"),
            "White Rating": game.get("white", {}).get("rating", "N/A"),
            "Black Player": game.get("black", {}).get("username", "Unknown"),
            "Black Rating": game.get("black", {}).get("rating", "N/A"),
            "Result": game_result,  # Processed as "Win", "Loss", or "Draw"
            "Main Opening": main_opening,  # Main opening from the text file
            "Variation": variation,  # Remaining part as variation
            "Information": pgn_split["Information"],  # Metadata
            "Moves": pgn_split["Moves"]  # Actual moves
        }
        if(game.get("rules", {}) == "chess"):
            game_list.append(game_entry)
    return game_list

def save_to_csv(data, filename):
    """
    Save data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename} (CSV format)")

def save_to_json(data, filename):
    """
    Save data to a beautified JSON file.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename} (JSON format)")

if __name__ == "__main__":
    username = "ardil30"  # Replace with your Chess.com username
    raw_file_path = f"./data/raw/{username}_raw_games.json"
    processed_json_path = f"./data/processed/{username}_games.json"
    processed_csv_path = f"./data/processed/{username}_games.csv"
    openings_file_path = "./data/processed/chess_openings.txt"

    # Ensure the processed data directory exists
    os.makedirs("./data/processed", exist_ok=True)

    # Load raw data
    with open(raw_file_path, "r") as file:
        raw_data = json.load(file)

    # Process data
    processed_data = process_game_data(raw_data, username, openings_file_path)

    # Save processed data
    save_to_json(processed_data, processed_json_path)
    save_to_csv(processed_data, processed_csv_path)
