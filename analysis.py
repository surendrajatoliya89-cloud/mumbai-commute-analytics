"""
analysis.py
-----------
Exploratory Data Analysis (EDA) for Mumbai Commute Analytics.
Generates statistical summaries and high-resolution Seaborn/Matplotlib charts.

Author: B.Sc Data Science Student Project
Academic Disclaimer:
This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/CLI rendering
import matplotlib.pyplot as plt
import seaborn as sns

def set_plot_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.labelsize"] = 11

def perform_eda(csv_path="data/commute_data_cleaned.csv", img_dir="static/images"):
    print("=" * 60)
    print("MUMBAI COMMUTE ANALYTICS — EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}. Run data_processing.py first!")

    os.makedirs(img_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    set_plot_style()

    # ---------------------------------------------------------
    # 1. SUMMARY STATISTICS PER TRANSPORT MODE
    # ---------------------------------------------------------
    print("\n--- 1. OVERALL TRANSPORT MODE SUMMARY ---")
    summary = df.groupby("Transport_Mode").agg(
        Count=("Commute_ID", "count"),
        Avg_Travel_Time_min=("Travel_Time_min", "mean"),
        Avg_Cost_INR=("Cost_INR", "mean"),
        Avg_Waiting_Time_min=("Waiting_Time_min", "mean"),
        Avg_Delay_min=("Delay_min", "mean"),
        Avg_Comfort=("Comfort_Rating", "mean"),
        Avg_User_Rating=("User_Rating", "mean"),
        Avg_Distance_km=("Distance_km", "mean")
    ).round(2)
    print(summary)

    # ---------------------------------------------------------
    # CHART 1: Multi-metric Transport Comparison (Time, Cost, Delay, Comfort)
    # ---------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    colors = {"Metro": "#0d6efd", "Local": "#dc3545", "Auto": "#ffc107"}

    # Subplot 1: Average Cost
    sns.barplot(data=df, x="Transport_Mode", y="Cost_INR", ax=axes[0, 0], palette=colors, errorbar=None)
    axes[0, 0].set_title("Average Cost (INR) by Transport Mode")
    axes[0, 0].set_ylabel("Cost (₹)")
    for p in axes[0, 0].patches:
        axes[0, 0].annotate(f"₹{p.get_height():.1f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                            ha='center', va='center', color='white' if p.get_height() > 50 else 'black', fontweight='bold')

    # Subplot 2: Average Travel Time
    sns.barplot(data=df, x="Transport_Mode", y="Travel_Time_min", ax=axes[0, 1], palette=colors, errorbar=None)
    axes[0, 1].set_title("Average Travel Time (Minutes)")
    axes[0, 1].set_ylabel("Travel Time (min)")
    for p in axes[0, 1].patches:
        axes[0, 1].annotate(f"{p.get_height():.1f}m", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                            ha='center', va='center', color='white', fontweight='bold')

    # Subplot 3: Average Waiting Time & Delay
    delay_df = df.groupby("Transport_Mode")[["Waiting_Time_min", "Delay_min"]].mean().reset_index()
    delay_melted = delay_df.melt(id_vars="Transport_Mode", var_name="Metric", value_name="Minutes")
    delay_melted["Metric"] = delay_melted["Metric"].map({"Waiting_Time_min": "Waiting Time", "Delay_min": "Traffic/Signal Delay"})
    sns.barplot(data=delay_melted, x="Transport_Mode", y="Minutes", hue="Metric", ax=axes[1, 0], palette="Blues_r")
    axes[1, 0].set_title("Average Waiting Time vs Delay")
    axes[1, 0].set_ylabel("Minutes")

    # Subplot 4: Comfort vs User Rating
    rating_df = df.groupby("Transport_Mode")[["Comfort_Rating", "User_Rating"]].mean().reset_index()
    rating_melted = rating_df.melt(id_vars="Transport_Mode", var_name="Metric", value_name="Score")
    rating_melted["Metric"] = rating_melted["Metric"].map({"Comfort_Rating": "Comfort (1-5)", "User_Rating": "User Rating (1-5)"})
    sns.barplot(data=rating_melted, x="Transport_Mode", y="Score", hue="Metric", ax=axes[1, 1], palette="Greens_r")
    axes[1, 1].set_title("Average Comfort and User Satisfaction Rating")
    axes[1, 1].set_ylim(0, 5.5)

    plt.tight_layout()
    chart1_path = os.path.join(img_dir, "transport_comparison.png")
    fig.savefig(chart1_path, dpi=180)
    plt.close(fig)
    print(f"[CHART 1 SAVED] {chart1_path}")

    # ---------------------------------------------------------
    # CHART 2: Distance vs Travel Time & Distance vs Cost
    # ---------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Scatter: Distance vs Travel Time
    sns.scatterplot(data=df, x="Distance_km", y="Travel_Time_min", hue="Transport_Mode", palette=colors, alpha=0.75, ax=axes[0])
    sns.lineplot(data=df, x="Distance_km", y="Travel_Time_min", hue="Transport_Mode", palette=colors, ax=axes[0], legend=False)
    axes[0].set_title("Distance (km) vs Travel Time (min)")
    axes[0].set_xlabel("Distance (km)")
    axes[0].set_ylabel("Travel Time (minutes)")

    # Scatter: Distance vs Cost
    sns.scatterplot(data=df, x="Distance_km", y="Cost_INR", hue="Transport_Mode", palette=colors, alpha=0.75, ax=axes[1])
    axes[1].set_title("Distance (km) vs Cost (INR)")
    axes[1].set_xlabel("Distance (km)")
    axes[1].set_ylabel("Cost (₹)")

    plt.tight_layout()
    chart2_path = os.path.join(img_dir, "distance_vs_time_cost.png")
    fig.savefig(chart2_path, dpi=180)
    plt.close(fig)
    print(f"[CHART 2 SAVED] {chart2_path}")

    # ---------------------------------------------------------
    # CHART 3: Peak vs Non-Peak Hour Travel Time Impact
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5))
    peak_comp = df.groupby(["Transport_Mode", "Peak_Hour"])["Travel_Time_min"].mean().reset_index()
    sns.barplot(data=peak_comp, x="Transport_Mode", y="Travel_Time_min", hue="Peak_Hour", palette=["#6c757d", "#dc3545"], ax=ax)
    ax.set_title("Peak-Hour Impact on Travel Time Across Transport Modes")
    ax.set_xlabel("Transport Mode")
    ax.set_ylabel("Average Travel Time (minutes)")
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f"{h:.1f}m", (p.get_x() + p.get_width() / 2., h / 2),
                        ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    plt.tight_layout()
    chart3_path = os.path.join(img_dir, "peak_hour_impact.png")
    fig.savefig(chart3_path, dpi=180)
    plt.close(fig)
    print(f"[CHART 3 SAVED] {chart3_path}")

    # ---------------------------------------------------------
    # CHART 4: Crowd Level Breakdown Across Transport Modes
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    crowd_order = ["Low", "Medium", "High", "Extreme"]
    crowd_counts = pd.crosstab(df["Transport_Mode"], df["Crowd_Level"], normalize="index")[crowd_order] * 100
    crowd_counts.plot(kind="bar", stacked=True, colormap="YlOrRd", ax=ax, edgecolor="black")
    ax.set_title("Crowd Level Distribution Percentage (%) by Transport Mode")
    ax.set_xlabel("Transport Mode")
    ax.set_ylabel("Percentage of Commutes (%)")
    ax.legend(title="Crowd Level", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.tight_layout()
    chart4_path = os.path.join(img_dir, "crowd_distribution.png")
    fig.savefig(chart4_path, dpi=180)
    plt.close(fig)
    print(f"[CHART 4 SAVED] {chart4_path}")

    # ---------------------------------------------------------
    # CHART 5: Route / Area Commute Analysis (Top High-Demand Routes)
    # ---------------------------------------------------------
    df["Route"] = df["Starting_Area"] + " → " + df["Destination"]
    top_routes = df.groupby("Route").agg(
        Trips=("Commute_ID", "count"),
        Avg_Time=("Travel_Time_min", "mean"),
        Avg_Cost=("Cost_INR", "mean")
    ).sort_values(by="Trips", ascending=False).head(8).reset_index()

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.barplot(data=top_routes, x="Avg_Time", y="Route", palette="coolwarm", ax=ax)
    ax.set_title("Average Travel Time on Top Frequent Commute Routes in Dataset")
    ax.set_xlabel("Average Travel Time (minutes)")
    ax.set_ylabel("Commute Route")
    for p in ax.patches:
        w = p.get_width()
        ax.annotate(f"{w:.1f} min", (w - 3.5, p.get_y() + p.get_height() / 2.),
                    ha='right', va='center', color='white', fontweight='bold', fontsize=9)
    plt.tight_layout()
    chart5_path = os.path.join(img_dir, "route_analysis.png")
    fig.savefig(chart5_path, dpi=180)
    plt.close(fig)
    print(f"[CHART 5 SAVED] {chart5_path}")

    print("\nEDA Completed! All 5 visualization charts generated in static/images/.")
    print("=" * 60)
    return summary

if __name__ == "__main__":
    perform_eda()

