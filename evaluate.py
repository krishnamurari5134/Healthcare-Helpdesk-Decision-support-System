"""Module owner: Aman Tiwari, Purpose: Evaluate model on test split, generate report and confusion matrix, Reviewed by: Krishna Murari"""
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from src.intent_classifier import load_dataset, split_data, build_model
from src import config

def main():
    df = load_dataset()
    x_train, x_test, y_train, y_test = split_data(df)
    
    model = build_model()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    
    report = classification_report(y_test, y_pred, zero_division=0)
    print("Classification Report:\n")
    print(report)
    
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = config.DOCS_DIR / "evaluation_report.txt"
    report_path.write_text(report, encoding="utf-8")
    
    labels = sorted(df["intent"].unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Intent Classifier Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45, ha="right")
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel("True Intent")
    plt.xlabel("Predicted Intent")
    
    cm_path = config.DOCS_DIR / "confusion_matrix.png"
    plt.savefig(cm_path, dpi=300)
    print(f"Evaluation report saved to {report_path}")
    print(f"Confusion matrix image saved to {cm_path}")

if __name__ == "__main__":
    main()
