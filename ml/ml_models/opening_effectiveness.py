import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """Load processed game data from JSON file."""
    return pd.read_json(file_path)

def feature_engineering(data):
    """Add features to enhance analysis."""
    data["Rating Differential"] = data["Black Rating"] - data["White Rating"]
    return data

def prepare_features_and_target(data):
    """Prepare features and target for opening analysis."""
    data = feature_engineering(data)

    # Define features and target
    features = ["Rating Differential" ,"Variation"]
    X = data[features]
    y = data["Result"].map({"Win": 2, "Draw": 1, "Loss": 0})

    # One-hot encode categorical features
    X = pd.get_dummies(X, columns=["Variation"])
    return X, y

def train_model(X_train, y_train):
    """Train a Random Forest Classifier."""
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        class_weight="balanced",
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and print metrics."""
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(
        y_test, y_pred, target_names=["Loss", "Draw", "Win"], zero_division=0
    ))

    # Plot confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Loss", "Draw", "Win"], yticklabels=["Loss", "Draw", "Win"])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    cm_path = "./ml/figures/opening_confusion_matrix.png"
    plt.savefig(cm_path)
    print(f"Confusion matrix saved to {cm_path}")
    plt.close()

def analyze_opening_effectiveness(data):
    """Analyze and visualize opening effectiveness."""
    opening_stats = data.groupby("Main Opening").apply(
        lambda x: pd.Series({
            "Win Rate": (x["Result"] == "Win").mean(),
            "Loss Rate": (x["Result"] == "Loss").mean(),
            "Draw Rate": (x["Result"] == "Draw").mean(),
            "Games Played": len(x)
        })
    )
    opening_stats = opening_stats.sort_values(by="Games Played", ascending=False)

    # Plotting the opening effectiveness
    opening_stats = opening_stats.head(20)  # Top 20 openings
    opening_stats[["Win Rate", "Loss Rate", "Draw Rate"]].plot(kind="bar", stacked=True, figsize=(12, 8))
    plt.title("Top 20 Openings Effectiveness")
    plt.xlabel("Opening")
    plt.ylabel("Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    bar_chart_path = "./ml/figures/opening_effectiveness.png"
    plt.savefig(bar_chart_path)
    print(f"Opening effectiveness chart saved to {bar_chart_path}")
    plt.close()

if __name__ == "__main__":
    # Paths
    data_path = "./data/processed/ardil30_games.json"

    # Load data
    print("Loading data...")
    data = load_data(data_path)

    # Prepare features and target
    print("Preparing features and target...")
    X, y = prepare_features_and_target(data)

    # Split data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print("Training model...")
    model = train_model(X_train, y_train)

    # Evaluate model
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)

    # Analyze opening effectiveness
    print("Analyzing opening effectiveness...")
    analyze_opening_effectiveness(data)

    # 53% accuracy 