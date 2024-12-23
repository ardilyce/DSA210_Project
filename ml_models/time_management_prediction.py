import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def load_data(file_path):
    """
    Load processed game data.
    """
    return pd.read_json(file_path)

def prepare_features_and_target(data):
    """
    Prepare features and target for the model.
    """
    features = data[["Time Class", "Average Time Per Move", "Player Rating"]]
    target = data["Result"].map({"Win": 1, "Draw": 0.5, "Loss": 0})  # Map result to numeric values
    features = pd.get_dummies(features, columns=["Time Class"])  # One-hot encode Time Class
    return features, target

def train_model(X_train, y_train):
    """
    Train a Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

if __name__ == "__main__":
    # Paths
    processed_data_path = "./data/processed/ardil30_games.json"

    # Load data
    print("Loading data...")
    data = load_data(processed_data_path)

    # Prepare features and target
    print("Preparing features and target...")
    X, y = prepare_features_and_target(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print("Training model...")
    model = train_model(X_train, y_train)

    # Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.4f}")
