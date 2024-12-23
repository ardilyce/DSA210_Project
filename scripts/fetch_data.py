import os
import requests
import json

# Define headers with User-Agent for API requests
headers = {
    'User-Agent': 'ChessDataFetcher/1.0 (ardilyuce@gmail.com)'  # Replace with your email
}

def fetch_game_archives(username):
    """
    Fetch the game archives URLs for the player.
    """
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching archives: HTTP {response.status_code}, {response.text}")
        return []
    archives = response.json().get('archives', [])
    print(f"Archives fetched: {len(archives)} archives found.")
    return archives

def fetch_games_from_archive(archive_url):
    """
    Fetch all games from a given archive URL.
    """
    response = requests.get(archive_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching games from {archive_url}: HTTP {response.status_code}, {response.text}")
        return []
    games = response.json().get('games', [])
    print(f"Games fetched from {archive_url}: {len(games)} games.")
    return games

def fetch_all_games(username):
    """
    Fetch all games by iterating through their game archives.
    """
    all_games = []
    archives = fetch_game_archives(username)
    if not archives:
        print("No archives fetched. Ensure the username is correct or the Chess.com API is accessible.")
        return all_games

    for archive_url in archives:
        print(f"Fetching games from archive: {archive_url}")
        games = fetch_games_from_archive(archive_url)
        all_games.extend(games)

    print(f"Total games fetched: {len(all_games)} games.")
    return all_games

def save_to_json(data, filename):
    """
    Save data to a beautified JSON file.
    """
    print(f"Saving data to {filename}...")
    if not data:
        print("No data to save. The file will not be updated.")
        return

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved successfully to {filename}. File size: {os.path.getsize(filename)} bytes")

if __name__ == "__main__":
    username = "ardil30"  # Chess.com username
    file_path = "./data/raw/ardil30_raw_games.json"

    # Ensure the raw data directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Fetch new games
    all_games = fetch_all_games(username)

    # Save fetched data
    save_to_json(all_games, file_path)
