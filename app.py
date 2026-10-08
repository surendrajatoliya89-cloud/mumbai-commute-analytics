"""
app.py
------
Flask Web Application for Mumbai Commute Analytics (Metro vs Local vs Auto).
A B.Sc Data Science College Project.

Academic Disclaimer:
This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics.
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "commute_data_cleaned.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "commute_model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "model", "model_metrics.json")

# Global data cache
df_cache = None
model_bundle = None

def load_data():
    global df_cache
    if df_cache is None:
        if os.path.exists(DATA_PATH):
            df_cache = pd.read_csv(DATA_PATH)
        else:
            df_cache = pd.DataFrame()
    return df_cache

def load_ml_model():
    global model_bundle
    if model_bundle is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model_bundle = pickle.load(f)
    return model_bundle

@app.route("/")
def home():
    df = load_data()
    total_trips = len(df) if not df.empty else 0
    return render_template("index.html", total_trips=total_trips)

@app.route("/dashboard")
def dashboard():
    df = load_data()
    if df.empty:
        return "Cleaned dataset not found! Please run data_processing.py first.", 500

    # KPI Metrics
    total_commutes = len(df)
    avg_travel_time = round(df["Travel_Time_min"].mean(), 1)
    avg_cost = round(df["Cost_INR"].mean(), 1)
    avg_distance = round(df["Distance_km"].mean(), 1)

    # Mode aggregations
    mode_counts = df["Transport_Mode"].value_counts().to_dict()
    most_used_transport = df["Transport_Mode"].mode()[0]

    # Mode speeds and costs
    mode_avg_time = df.groupby("Transport_Mode")["Travel_Time_min"].mean().to_dict()
    mode_avg_cost = df.groupby("Transport_Mode")["Cost_INR"].mean().to_dict()

    fastest_transport = min(mode_avg_time, key=mode_avg_time.get)
    cheapest_transport = min(mode_avg_cost, key=mode_avg_cost.get)

    # Chart data for Chart.js
    chart_modes = list(mode_counts.keys())
    chart_counts = [mode_counts[m] for m in chart_modes]

    peak_counts = df["Peak_Hour"].value_counts().to_dict()

    return render_template(
        "dashboard.html",
        total_commutes=total_commutes,
        avg_travel_time=avg_travel_time,
        avg_cost=avg_cost,
        avg_distance=avg_distance,
        most_used_transport=most_used_transport,
        fastest_transport=fastest_transport,
        cheapest_transport=cheapest_transport,
        mode_counts=mode_counts,
        mode_avg_time=mode_avg_time,
        mode_avg_cost=mode_avg_cost,
        chart_modes=chart_modes,
        chart_counts=chart_counts,
        peak_counts=peak_counts
    )

@app.route("/comparison")
def comparison():
    df = load_data()
    if df.empty:
        return "Dataset not found", 500

    # Detailed Mode Groupings
    comp = df.groupby("Transport_Mode").agg(
        Trips=("Commute_ID", "count"),
        Avg_Distance=("Distance_km", "mean"),
        Avg_Time=("Travel_Time_min", "mean"),
        Avg_Cost=("Cost_INR", "mean"),
        Avg_Cost_Per_Km=("Cost_Per_Km", "mean"),
        Avg_Waiting=("Waiting_Time_min", "mean"),
        Avg_Delay=("Delay_min", "mean"),
        Avg_Comfort=("Comfort_Rating", "mean"),
        Avg_Rating=("User_Rating", "mean")
    ).round(2).to_dict(orient="index")

    modes = list(comp.keys())
    times = [comp[m]["Avg_Time"] for m in modes]
    costs = [comp[m]["Avg_Cost"] for m in modes]
    comfort = [comp[m]["Avg_Comfort"] for m in modes]
    ratings = [comp[m]["Avg_Rating"] for m in modes]

    return render_template(
        "comparison.html",
        comp=comp,
        modes=modes,
        times=times,
        costs=costs,
        comfort=comfort,
        ratings=ratings
    )

@app.route("/data")
def data_view():
    df = load_data()
    if df.empty:
        return "Dataset not found", 500

    # Filtering parameters from query string
    selected_mode = request.args.get("mode", "All")
    selected_peak = request.args.get("peak", "All")
    selected_weather = request.args.get("weather", "All")

    filtered_df = df.copy()
    if selected_mode != "All":
        filtered_df = filtered_df[filtered_df["Transport_Mode"] == selected_mode]
    if selected_peak != "All":
        filtered_df = filtered_df[filtered_df["Peak_Hour"] == selected_peak]
    if selected_weather != "All":
        filtered_df = filtered_df[filtered_df["Weather"] == selected_weather]

    # Show top 100 rows for display performance
    table_data = filtered_df.head(100).to_dict(orient="records")
    total_matching = len(filtered_df)

    return render_template(
        "data.html",
        records=table_data,
        total_matching=total_matching,
        selected_mode=selected_mode,
        selected_peak=selected_peak,
        selected_weather=selected_weather
    )

@app.route("/analytics")
def analytics():
    # Read metrics JSON if available
    metrics = {}
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)

    return render_template("analytics.html", metrics=metrics)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    bundle = load_ml_model()
    prediction_result = None
    prediction_proba = None
    error_msg = None
    input_data = {}

    if request.method == "POST":
        try:
            distance = float(request.form.get("distance", 10.0))
            travel_time = float(request.form.get("travel_time", 35.0))
            waiting_time = float(request.form.get("waiting_time", 5.0))
            cost = float(request.form.get("cost", 30.0))
            peak_hour = request.form.get("peak_hour", "No")
            crowd_level = request.form.get("crowd_level", "Medium")
            weather = request.form.get("weather", "Clear")
            delay = float(request.form.get("delay", 2.0))
            comfort = int(request.form.get("comfort", 3))

            input_data = {
                "distance": distance,
                "travel_time": travel_time,
                "waiting_time": waiting_time,
                "cost": cost,
                "peak_hour": peak_hour,
                "crowd_level": crowd_level,
                "weather": weather,
                "delay": delay,
                "comfort": comfort
            }

            if bundle is not None:
                model = bundle["model"]
                mappings = bundle["mappings"]
                class_names = bundle["class_names"]

                # Transform input to encoded feature array matching model training
                encoded_row = [
                    distance,
                    travel_time,
                    waiting_time,
                    cost,
                    mappings["peak_map"].get(peak_hour, 0),
                    mappings["crowd_map"].get(crowd_level, 1),
                    delay,
                    mappings["weather_map"].get(weather, 0),
                    comfort
                ]

                feature_df = pd.DataFrame([encoded_row], columns=bundle["feature_cols"])
                pred_idx = model.predict(feature_df)[0]
                prediction_result = class_names[pred_idx]

                # Probabilities
                probabilities = model.predict_proba(feature_df)[0]
                prediction_proba = {
                    class_names[i]: round(probabilities[i] * 100, 1)
                    for i in range(len(class_names))
                }
            else:
                error_msg = "Model artifact not loaded. Please run train_model.py first."
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"

    return render_template(
        "prediction.html",
        prediction_result=prediction_result,
        prediction_proba=prediction_proba,
        input_data=input_data,
        error_msg=error_msg
    )

@app.route("/about")
def about():
    metrics = {}
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
    return render_template("about.html", metrics=metrics)

# API endpoint for chart data or external queries
@app.route("/api/summary")
def api_summary():
    df = load_data()
    if df.empty:
        return jsonify({"error": "No data available"}), 404
    summary = df.groupby("Transport_Mode").agg(
        Trips=("Commute_ID", "count"),
        Avg_Time=("Travel_Time_min", "mean"),
        Avg_Cost=("Cost_INR", "mean")
    ).round(2).to_dict(orient="index")
    return jsonify(summary)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

