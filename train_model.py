"""
train_model.py
--------------
Machine Learning Pipeline for Mumbai Commute Mode Prediction.
Trains Decision Tree and Random Forest Classifiers, evaluates performance,
and saves the trained model to model/commute_model.pkl.

Author: B.Sc Data Science Student Project
Academic Disclaimer:
This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics.
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

def train_and_evaluate(csv_path="data/commute_data_cleaned.csv", model_dir="model", img_dir="static/images"):
    print("=" * 60)
    print("MUMBAI COMMUTE ANALYTICS — MACHINE LEARNING PIPELINE")
    print("=" * 60)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}. Run data_processing.py first!")

    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    
    df = pd.read_csv(csv_path)
    print(f"[1] Loaded dataset with {len(df)} samples.")

    # ---------------------------------------------------------
    # 1. FEATURE SELECTION & PREPROCESSING
    # ---------------------------------------------------------
    feature_cols = [
        "Distance_km", 
        "Travel_Time_min", 
        "Waiting_Time_min", 
        "Cost_INR", 
        "Peak_Hour", 
        "Crowd_Level", 
        "Delay_min", 
        "Weather", 
        "Comfort_Rating"
    ]
    target_col = "Transport_Mode"

    X_raw = df[feature_cols].copy()
    y_raw = df[target_col].copy()

    # Encode categorical features with explicit mappings for reproducibility
    # Peak_Hour: No -> 0, Yes -> 1
    # Crowd_Level: Low -> 0, Medium -> 1, High -> 2, Extreme -> 3
    # Weather: Clear -> 0, Overcast -> 1, Rainy -> 2
    crowd_map = {"Low": 0, "Medium": 1, "High": 2, "Extreme": 3}
    peak_map = {"No": 0, "Yes": 1}
    weather_map = {"Clear": 0, "Overcast": 1, "Rainy": 2}

    X = X_raw.copy()
    X["Crowd_Level"] = X["Crowd_Level"].map(crowd_map).fillna(1)
    X["Peak_Hour"] = X["Peak_Hour"].map(peak_map).fillna(0)
    X["Weather"] = X["Weather"].map(weather_map).fillna(0)

    # Encode Target
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    class_names = list(le.classes_)
    print(f"    Target classes encoded: {dict(enumerate(class_names))}")

    # ---------------------------------------------------------
    # 2. TRAIN-TEST SPLIT (80% Train, 20% Test)
    # ---------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[2] Train-Test Split Completed:")
    print(f"    Training samples:   {len(X_train)} (80%)")
    print(f"    Testing samples:    {len(X_test)} (20%)")

    # ---------------------------------------------------------
    # 3. MODEL 1: DECISION TREE CLASSIFIER (Primary Explainable Model)
    # ---------------------------------------------------------
    print("\n[3] Training Decision Tree Classifier (max_depth=5)...")
    dt_model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)
    acc_dt = accuracy_score(y_test, y_pred_dt)
    print(f"    Decision Tree Accuracy: {acc_dt * 100:.2f}%")

    # ---------------------------------------------------------
    # 4. MODEL 2: RANDOM FOREST CLASSIFIER (Comparison Ensemble Model)
    # ---------------------------------------------------------
    print("\n[4] Training Random Forest Classifier (n_estimators=100)...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"    Random Forest Accuracy: {acc_rf * 100:.2f}%")

    # ---------------------------------------------------------
    # 5. MODEL EVALUATION & REPORTS
    # ---------------------------------------------------------
    print("\n[5] Decision Tree Classification Report:")
    report_dict = classification_report(y_test, y_pred_dt, target_names=class_names, output_dict=True)
    print(classification_report(y_test, y_pred_dt, target_names=class_names))

    cm = confusion_matrix(y_test, y_pred_dt)
    print("    Decision Tree Confusion Matrix:")
    print(cm)

    # ---------------------------------------------------------
    # 6. VISUALIZATION 1: CONFUSION MATRIX PLOT
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_title(f"Decision Tree Confusion Matrix\nAccuracy: {acc_dt*100:.1f}%")
    ax.set_xlabel("Predicted Mode")
    ax.set_ylabel("Actual Ground Truth Mode")
    plt.tight_layout()
    cm_path = os.path.join(img_dir, "confusion_matrix.png")
    fig.savefig(cm_path, dpi=180)
    plt.close(fig)
    print(f"    Confusion Matrix saved: {cm_path}")

    # ---------------------------------------------------------
    # 7. VISUALIZATION 2: FEATURE IMPORTANCE PLOT
    # ---------------------------------------------------------
    feat_importances = pd.Series(dt_model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=feat_importances.values, y=feat_importances.index, palette="viridis", ax=ax)
    ax.set_title("Decision Tree Feature Importance")
    ax.set_xlabel("Gini Importance Score")
    ax.set_ylabel("Input Feature")
    for p in ax.patches:
        val = p.get_width()
        if val > 0.01:
            ax.annotate(f"{val*100:.1f}%", (val + 0.01, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    fi_path = os.path.join(img_dir, "feature_importance.png")
    fig.savefig(fi_path, dpi=180)
    plt.close(fig)
    print(f"    Feature Importance saved: {fi_path}")

    # ---------------------------------------------------------
    # 8. SAVE TRAINED MODEL & ARTIFACTS
    # ---------------------------------------------------------
    bundle = {
        "model": dt_model,
        "rf_model": rf_model,
        "label_encoder": le,
        "feature_cols": feature_cols,
        "mappings": {
            "crowd_map": crowd_map,
            "peak_map": peak_map,
            "weather_map": weather_map
        },
        "accuracy_dt": float(acc_dt),
        "accuracy_rf": float(acc_rf),
        "class_names": class_names
    }
    
    model_path = os.path.join(model_dir, "commute_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(bundle, f)
    print(f"\n[6] Saved model artifact: {model_path}")

    # Save metrics JSON for web display
    metrics_data = {
        "dt_accuracy": round(acc_dt * 100, 2),
        "rf_accuracy": round(acc_rf * 100, 2),
        "total_test_samples": len(y_test),
        "feature_importance": {k: round(v * 100, 2) for k, v in feat_importances.items()},
        "classification_report": {
            cls: {
                "precision": round(report_dict[cls]["precision"], 2),
                "recall": round(report_dict[cls]["recall"], 2),
                "f1_score": round(report_dict[cls]["f1-score"], 2),
                "support": int(report_dict[cls]["support"])
            }
            for cls in class_names
        }
    }
    metrics_path = os.path.join(model_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=4)
    print(f"    Saved metrics JSON: {metrics_path}")
    print("=" * 60)

    return bundle

if __name__ == "__main__":
    train_and_evaluate()

