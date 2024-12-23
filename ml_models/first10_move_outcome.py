import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import itertools

def load_data(file_path):
    """
    Load processed game data from JSON file.
    """
    return pd.read_json(file_path)

def split_data(data, train_ratio=0.8):
    """
    Shuffle and split data into training and testing sets.
    """
    data = data.sample(frac=1)  # Shuffle data
    train_size = int(len(data) * train_ratio)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data

def prepare_features_and_target(train_data, test_data):
    """
    Prepare features and target for training and testing.
    """
    # Define features and target
    X_train = train_data[["White Rating", "Black Rating", "Time Class", "Main Opening"]]
    y_train = train_data["Result"].map({"Win": 2, "Draw": 1, "Loss": 0})

    X_test = test_data[["White Rating", "Black Rating", "Time Class", "Main Opening"]]
    y_test = test_data["Result"].map({"Win": 2, "Draw": 1, "Loss": 0})

    # One-hot encode categorical features
    X_train = pd.get_dummies(X_train, columns=["Time Class", "Main Opening"])
    X_test = pd.get_dummies(X_test, columns=["Time Class", "Main Opening"])

    # Align test set to match training set columns
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, use_smote=False):
    """
    Train a Random Forest Classifier with customized class weights.
    """
    # Adjust class weights to focus more on Win and Loss
    class_weights = {0: 1, 1: 0.3, 2: 1}  # More weight on Win and Loss, less on Draw

    # Optionally apply SMOTE for class imbalance, but ignore draws
    if use_smote:
        print("Applying SMOTE oversampling...")
        smote = SMOTE(random_state=42, sampling_strategy={0: 1, 2: 1})  # Don't oversample Draw
        X_train, y_train = smote.fit_resample(X_train, y_train)

    # Train Random Forest Classifier with custom class weights
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(class_weight=class_weights, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model and print metrics.
    """
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    return y_test, y_pred

def plot_confusion_matrix(y_test, y_pred, labels, save_path):
    """
    Plot and save a confusion matrix.
    """
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = range(len(labels))
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Confusion matrix saved to {save_path}")
    plt.close()

def save_model(model, model_path):
    """
    Save the trained model to a file.
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Paths
    data_path = "./data/processed/ardil30_games.json"
    model_path = "./models/game_outcome_predictor.pkl"
    cm_path = "./reports/figures/first10_move_confusion_matrix.png"

    # Load data
    print("Loading data...")
    data = load_data(data_path)

    # Split data into training (80%) and testing (20%) sets
    print("Splitting data...")
    train_data, test_data = split_data(data, train_ratio=0.8)

    # Prepare features and target
    print("Preparing features and target...")
    X_train, X_test, y_train, y_test = prepare_features_and_target(train_data, test_data)

    # Train model
    print("Training model...")
    model = train_model(X_train, y_train, use_smote=False)  # Set use_smote=True if you want to apply SMOTE

    # Evaluate model
    print("Evaluating model...")
    y_test, y_pred = evaluate_model(model, X_test, y_test)

    # Plot confusion matrix
    print("Generating confusion matrix...")
    plot_confusion_matrix(y_test, y_pred, labels=["Loss", "Draw", "Win"], save_path=cm_path)

    # Save model
    print("Saving model...")
    save_model(model, model_path)
