"""Module owner: Krishna Murari, Purpose: Command-line script to train and save the intent model, Reviewed by: Aman Tiwari"""
from sklearn.metrics import accuracy_score
from src import config
from src.intent_classifier import build_model, load_dataset, split_data, train_and_save

def main():
    df = load_dataset()
    print(f"Loaded {len(df)} queries from {config.QUERIES_CSV.name}")
    print(df["intent"].value_counts().to_string(), "\n")
    
    x_train, x_test, y_train, y_test = split_data(df)
    check_model = build_model()
    check_model.fit(x_train, y_train)
    accuracy = accuracy_score(y_test, check_model.predict(x_test))
    print(f"Train size: {len(x_train)}, Test size: {len(x_test)}")
    print(f"Test accuracy: {accuracy:.2%}")
    
    train_and_save()
    print(f"Model saved to {config.MODEL_PATH}")

if __name__ == "__main__":
    main()
