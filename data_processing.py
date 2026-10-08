"""
data_processing.py
------------------
Data Cleaning and Preprocessing Pipeline for Mumbai Commute Analytics.

Author: B.Sc Data Science Student Project
Academic Disclaimer:
This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics.
"""

import os
import pandas as pd
import numpy as np

def clean_commute_data(input_csv_path="data/commute_data.csv", output_csv_path="data/commute_data_cleaned.csv"):
    print("=" * 60)
    print("MUMBAI COMMUTE ANALYTICS — DATA CLEANING PIPELINE")
    print("=" * 60)
    
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input file not found at: {input_csv_path}")
        
    df = pd.read_csv(input_csv_path)
    initial_rows = len(df)
    print(f"[STEP 1] Loaded raw data: {initial_rows} records, {df.shape[1]} columns.")
    
    # ---------------------------------------------------------
    # 1. REMOVE DUPLICATE RECORDS
    # ---------------------------------------------------------
    duplicates_count = df.duplicated().sum()
    print(f"[STEP 2] Checking for duplicate records: Found {duplicates_count} duplicates.")
    df = df.drop_duplicates()
    print(f"         Removed duplicates. Remaining records: {len(df)}")

    # ---------------------------------------------------------
    # 2. STANDARDIZE CATEGORICAL VALUES (Transport_Mode)
    # ---------------------------------------------------------
    print("[STEP 3] Standardizing Transport_Mode naming...")
    print("         Values before cleaning:", df["Transport_Mode"].unique())
    
    # Strip whitespace, lowercase, and map to clean canonical labels
    def standardize_mode(mode_val):
        if pd.isna(mode_val):
            return "Local"
        cleaned = str(mode_val).strip().lower()
        if "metro" in cleaned:
            return "Metro"
        elif "local" in cleaned or "train" in cleaned:
            return "Local"
        elif "auto" in cleaned or "rickshaw" in cleaned:
            return "Auto"
        return "Local"

    df["Transport_Mode"] = df["Transport_Mode"].apply(standardize_mode)
    print("         Values after cleaning:", df["Transport_Mode"].unique())

    # ---------------------------------------------------------
    # 3. DETECT & REMOVE IMPOSSIBLE NUMERICAL VALUES / ANOMALIES
    # ---------------------------------------------------------
    print("[STEP 4] Filtering out impossible values and extreme outliers...")
    before_anomalies = len(df)
    
    # Cost, travel time, and distance must be strictly positive
    # Delay and waiting time must be non-negative
    # Maximum reasonable commute distance within Mumbai MMR is ~70 km
    valid_mask = (
        (df["Distance_km"] > 0) & (df["Distance_km"] <= 70) &
        (df["Travel_Time_min"] > 0) & (df["Travel_Time_min"] <= 300) &
        (df["Cost_INR"] > 0) &
        ((df["Delay_min"].isna()) | (df["Delay_min"] >= 0)) &
        ((df["Waiting_Time_min"].isna()) | (df["Waiting_Time_min"] >= 0))
    )
    df = df[valid_mask].copy()
    dropped_anomalies = before_anomalies - len(df)
    print(f"         Filtered out {dropped_anomalies} records with negative/impossible values.")

    # ---------------------------------------------------------
    # 4. HANDLE MISSING VALUES (IMPUTATION)
    # ---------------------------------------------------------
    print("[STEP 5] Checking and handling missing values (NaN)...")
    print("         Missing values before imputation:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    # Impute Waiting_Time_min using Median of each Transport_Mode
    wait_medians = df.groupby("Transport_Mode")["Waiting_Time_min"].transform("median")
    df["Waiting_Time_min"] = df["Waiting_Time_min"].fillna(wait_medians)
    # In case any remains, fill with overall median
    df["Waiting_Time_min"] = df["Waiting_Time_min"].fillna(df["Waiting_Time_min"].median()).round().astype(int)

    # Impute Crowd_Level using Mode (most frequent) of Transport_Mode + Peak_Hour
    mode_crowd = df.groupby(["Transport_Mode", "Peak_Hour"])["Crowd_Level"].transform(
        lambda s: s.mode()[0] if not s.mode().empty else "Medium"
    )
    df["Crowd_Level"] = df["Crowd_Level"].fillna(mode_crowd)
    df["Crowd_Level"] = df["Crowd_Level"].fillna("Medium")

    # ---------------------------------------------------------
    # 5. DATA TYPE CONVERSIONS
    # ---------------------------------------------------------
    print("[STEP 6] Standardizing data types...")
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df["Distance_km"] = df["Distance_km"].astype(float).round(1)
    df["Travel_Time_min"] = df["Travel_Time_min"].astype(int)
    df["Waiting_Time_min"] = df["Waiting_Time_min"].astype(int)
    df["Cost_INR"] = df["Cost_INR"].astype(int)
    df["Delay_min"] = df["Delay_min"].astype(int)
    df["Comfort_Rating"] = df["Comfort_Rating"].astype(int)
    df["User_Rating"] = df["User_Rating"].astype(int)

    # ---------------------------------------------------------
    # 6. FEATURE ENGINEERING / COMMUTE METRICS
    # ---------------------------------------------------------
    # Add useful derived metrics for deeper Data Science analysis
    df["Total_Trip_Time_min"] = df["Travel_Time_min"] + df["Waiting_Time_min"]
    df["Cost_Per_Km"] = (df["Cost_INR"] / df["Distance_km"]).round(2)
    df["Speed_kmh"] = ((df["Distance_km"] / (df["Travel_Time_min"] / 60))).round(1)

    # Reset Index
    df = df.reset_index(drop=True)

    # ---------------------------------------------------------
    # 7. SAVE CLEANED DATASET
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    
    print("-" * 60)
    print(f"Data Cleaning Completed Successfully!")
    print(f"Initial raw rows:     {initial_rows}")
    print(f"Final cleaned rows:   {len(df)}")
    print(f"Rows dropped:         {initial_rows - len(df)}")
    print(f"Cleaned file saved:   {output_csv_path}")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    clean_commute_data()

