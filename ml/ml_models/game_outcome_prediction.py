import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    # Load processed game data from JSON file.
    return pd.read_json(file_path)

def split_data(data, train_ratio=0.8):
    # Shuffle and split data into training and testing sets.
    data = data.sample(frac=1, random_state=42)  # Shuffle data
    train_size = int(len(data) * train_ratio)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data

def feature_engineering(data):
    # Add new features to enhance model performance.
    data["Rating Differential"] = data["Black Rating"] - data["White Rating"]
    return data

def prepare_features_and_target(train_data, test_data):
    # Prepare features and target for training and testing.
    train_data = feature_engineering(train_data)
    test_data = feature_engineering(test_data)

    # Define features and target
    features = ["White Rating", "Black Rating", "Rating Differential", "Time Class", "Main Opening"]
    X_train = train_data[features]
    y_train = train_data["Result"].map({"Win": 2, "Draw": 1, "Loss": 0})

    X_test = test_data[features]
    y_test = test_data["Result"].map({"Win": 2, "Draw": 1, "Loss": 0})

    # One-hot encode categorical features
    X_train = pd.get_dummies(X_train, columns=["Time Class", "Main Opening"])
    X_test = pd.get_dummies(X_test, columns=["Time Class", "Main Opening"])

    # Align test set to match training set columns
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, use_smote=False):
    # Train a Random Forest Classifier, optionally using balanced SMOTE for oversampling.
    if use_smote:
        print("Applying SMOTE with balanced sampling strategy...")
        smote = SMOTE(
            sampling_strategy={0: len(y_train[y_train == 0]), 
                               1: len(y_train[y_train == 1]) * 2, 
                               2: len(y_train[y_train == 2])}, 
            random_state=42
        )
        X_train, y_train = smote.fit_resample(X_train, y_train)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        class_weight={0: 1, 1: 1, 2: 1},  
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    # Evaluate the model and print metrics.
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
    cm_path = "./ml/figures/confusion_matrix.png"
    plt.savefig(cm_path)
    print(f"Confusion matrix saved to {cm_path}")
    plt.close()

def save_model(model, model_path):
    # Save the trained model to a file.
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Paths
    data_path = "./data/processed/ardil30_games.json"
    model_path = "./ml/models/game_outcome_predictor.pkl"

    # Load data
    print("Loading data...")
    data = load_data(data_path)

    # Split data
    print("Splitting data...")
    train_data, test_data = split_data(data, train_ratio=0.8)

    # Prepare features and target
    print("Preparing features and target...")
    X_train, X_test, y_train, y_test = prepare_features_and_target(train_data, test_data)

    # Train model
    print("Training model...")
    model = train_model(X_train, y_train, use_smote=True)

    # Evaluate model
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)

    # Save model
    print("Saving model...")
    save_model(model, model_path)
