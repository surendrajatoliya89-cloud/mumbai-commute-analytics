"""
generate_dataset.py
-------------------
Academic Simulation Script for Mumbai Commute Dataset.

DISCLAIMER:
This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_commute_dataset(n_samples=1200, random_seed=42):
    random.seed(random_seed)
    np.random.seed(random_seed)

    areas = [
        "Andheri", "Borivali", "Dadar", "Bandra", "Thane", 
        "Churchgate", "Ghatkopar", "Kurla", "BKC", "Colaba", 
        "Malad", "Vashi", "Powai", "Goregaon"
    ]

    # Approximate pairwise distance matrix estimates (km)
    distances = {
        ("Borivali", "Churchgate"): 38,
        ("Borivali", "Andheri"): 14,
        ("Borivali", "Dadar"): 28,
        ("Borivali", "Bandra"): 22,
        ("Borivali", "Malad"): 5,
        ("Borivali", "Goregaon"): 8,
        ("Andheri", "Churchgate"): 25,
        ("Andheri", "Bandra"): 9,
        ("Andheri", "BKC"): 11,
        ("Andheri", "Ghatkopar"): 12,
        ("Andheri", "Powai"): 8,
        ("Andheri", "Dadar"): 16,
        ("Andheri", "Malad"): 9,
        ("Bandra", "Churchgate"): 16,
        ("Bandra", "BKC"): 4,
        ("Bandra", "Dadar"): 7,
        ("Bandra", "Kurla"): 6,
        ("Dadar", "Churchgate"): 10,
        ("Dadar", "Colaba"): 13,
        ("Dadar", "Kurla"): 8,
        ("Dadar", "Thane"): 26,
        ("Thane", "Kurla"): 19,
        ("Thane", "Ghatkopar"): 15,
        ("Thane", "Dadar"): 26,
        ("Ghatkopar", "Kurla"): 4,
        ("Ghatkopar", "BKC"): 9,
        ("Kurla", "BKC"): 3,
        ("Vashi", "Kurla"): 16,
        ("Vashi", "Dadar"): 23,
        ("Colaba", "Churchgate"): 3,
        ("Powai", "Ghatkopar"): 6,
        ("Powai", "BKC"): 12
    }

    start_date = datetime(2024, 1, 1)
    records = []

    for i in range(1, n_samples + 1):
        commute_id = f"MUM_{1000 + i}"
        
        # Random date within 90 days
        day_offset = random.randint(0, 90)
        curr_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        
        start_area = random.choice(areas)
        dest_area = random.choice([a for a in areas if a != start_area])
        
        # Distance calculation
        key = (start_area, dest_area)
        rev_key = (dest_area, start_area)
        if key in distances:
            base_dist = distances[key]
        elif rev_key in distances:
            base_dist = distances[rev_key]
        else:
            base_dist = random.randint(5, 30)
        
        distance = round(max(2.0, base_dist + random.uniform(-1.5, 2.5)), 1)
        
        # Peak Hour (approx 55% peak commute simulation)
        is_peak = random.choice(["Yes", "Yes", "No", "No", "Yes"])
        peak_factor = 1.35 if is_peak == "Yes" else 1.0
        
        # Weather
        weather = random.choices(["Clear", "Overcast", "Rainy"], weights=[0.65, 0.20, 0.15])[0]
        weather_delay = 8 if weather == "Rainy" else (2 if weather == "Overcast" else 0)

        # Mode selection logic based on distance & urban feasibility
        if distance > 22:
            # Long distance favors Local train, rarely Auto
            mode_choice = random.choices(["Local", "Metro", "Auto"], weights=[0.75, 0.20, 0.05])[0]
        elif distance > 10:
            # Medium distance favors Metro & Local
            mode_choice = random.choices(["Metro", "Local", "Auto"], weights=[0.45, 0.40, 0.15])[0]
        else:
            # Short distance
            mode_choice = random.choices(["Auto", "Metro", "Local"], weights=[0.50, 0.35, 0.15])[0]

        # Mode dynamics
        if mode_choice == "Local":
            # Very cheap (₹5 to ₹25), fast long-distance, high crowds during peak
            cost = int(min(25, max(5, 5 + (distance * 0.4))))
            speed_kmh = random.uniform(32, 42)
            travel_time = round((distance / speed_kmh) * 60 * (1.1 if is_peak == "Yes" else 1.0))
            waiting_time = random.randint(4, 15)
            delay = random.randint(0, 15) + (5 if is_peak == "Yes" else 0) + weather_delay
            
            if is_peak == "Yes":
                crowd = random.choices(["High", "Extreme"], weights=[0.3, 0.7])[0]
                comfort = random.choice([1, 2])
            else:
                crowd = random.choices(["Low", "Medium", "High"], weights=[0.3, 0.5, 0.2])[0]
                comfort = random.choice([2, 3, 4])
            user_rating = random.choice([3, 4, 3, 2, 4])

        elif mode_choice == "Metro":
            # Moderate cost (₹20 to ₹60), air-conditioned, reliable speed, low delays
            cost = int(min(60, max(20, 20 + (distance * 1.5))))
            speed_kmh = random.uniform(30, 36)
            travel_time = round((distance / speed_kmh) * 60)
            waiting_time = random.randint(3, 7)
            delay = random.randint(0, 5) + (1 if weather == "Rainy" else 0)
            
            if is_peak == "Yes":
                crowd = random.choices(["Medium", "High"], weights=[0.4, 0.6])[0]
                comfort = random.choice([3, 4])
            else:
                crowd = random.choices(["Low", "Medium"], weights=[0.6, 0.4])[0]
                comfort = random.choice([4, 5])
            user_rating = random.choice([4, 5, 4, 5, 3])

        else: # Auto
            # Expensive (₹23 first 1.5km + ₹15.3/km approx), traffic sensitive
            cost = int(round(23 + max(0, distance - 1.5) * random.uniform(15.0, 16.5)))
            # Speed drops heavily in peak hours and rain
            speed_kmh = random.uniform(14, 24) / peak_factor
            if weather == "Rainy":
                speed_kmh *= 0.85
            travel_time = round((distance / speed_kmh) * 60)
            waiting_time = random.randint(3, 14) if is_peak == "Yes" else random.randint(2, 6)
            delay = random.randint(4, 25) if is_peak == "Yes" else random.randint(0, 8)
            delay += weather_delay
            crowd = "Low" # Only 1-3 passengers in auto
            comfort = random.choice([3, 4]) if is_peak == "No" else random.choice([2, 3])
            user_rating = random.choice([3, 4, 3, 2, 4])

        # Total travel time adjustment
        travel_time = max(8, travel_time + delay)

        records.append({
            "Commute_ID": commute_id,
            "Date": curr_date,
            "Starting_Area": start_area,
            "Destination": dest_area,
            "Transport_Mode": mode_choice,
            "Distance_km": distance,
            "Travel_Time_min": travel_time,
            "Waiting_Time_min": waiting_time,
            "Cost_INR": cost,
            "Peak_Hour": is_peak,
            "Crowd_Level": crowd,
            "Delay_min": delay,
            "Weather": weather,
            "Comfort_Rating": comfort,
            "User_Rating": user_rating
        })

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # INTENTIONAL DIRTY DATA INJECTION FOR REALISTIC DATA CLEANING:
    # -------------------------------------------------------------
    # 1. Duplicate rows (~20 duplicate rows)
    dup_rows = df.sample(n=20, random_state=12)
    df = pd.concat([df, dup_rows], ignore_index=True)

    # 2. String inconsistencies in Transport_Mode (lowercase, spaces)
    messy_indices = df.sample(n=35, random_state=42).index
    for idx in messy_indices[:12]:
        df.loc[idx, "Transport_Mode"] = "metro"
    for idx in messy_indices[12:24]:
        df.loc[idx, "Transport_Mode"] = "  Local  "
    for idx in messy_indices[24:]:
        df.loc[idx, "Transport_Mode"] = "auto rickshaw"

    # 3. Missing values (NaNs in Waiting_Time_min and Crowd_Level)
    nan_wait_idx = df.sample(n=25, random_state=99).index
    df.loc[nan_wait_idx, "Waiting_Time_min"] = np.nan

    nan_crowd_idx = df.sample(n=18, random_state=101).index
    df.loc[nan_crowd_idx, "Crowd_Level"] = np.nan

    # 4. Outliers/Impossible values (e.g., negative cost or negative delay)
    bad_val_idx = df.sample(n=6, random_state=202).index
    df.loc[bad_val_idx[0], "Cost_INR"] = -15
    df.loc[bad_val_idx[1], "Travel_Time_min"] = -5
    df.loc[bad_val_idx[2], "Distance_km"] = 999.0 # Impossible distance inside Mumbai
    df.loc[bad_val_idx[3], "Delay_min"] = -10
    df.loc[bad_val_idx[4], "Waiting_Time_min"] = -2
    df.loc[bad_val_idx[5], "Cost_INR"] = 0

    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "commute_data.csv")
    df = generate_commute_dataset(n_samples=1200)
    df.to_csv(out_path, index=False)
    print(f"Generated raw dataset successfully: {out_path}")
    print(f"Dataset shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nIntentional Dirty Data Check:")
    print("Null values per column:")
    print(df.isnull().sum())
    print("Duplicate count:", df.duplicated().sum())

