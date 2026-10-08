# Mumbai Commute Analytics — Metro vs Local vs Auto
**A Beginner-Friendly B.Sc Data Science College Project**

---

## 1. Project Objective
This project builds an empirical Data Science and Machine Learning system that analyses Mumbai commuting dynamics and compares three major transit modes:
- **Mumbai Metro**
- **Mumbai Suburban Local Train**
- **Auto Rickshaw**

The system investigates travel time, fare costs, travel distance, waiting times, traffic bottlenecks during peak hours, crowding levels, comfort ratings, and commuter preferences. An explainable **Decision Tree Classifier** (alongside a **Random Forest Classifier**) is trained to predict the most suitable transport mode for any journey.

> **Academic Project Disclaimer:**  
> *"This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics."*

---

## 2. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Backend:** Python 3, Flask microframework
- **Data Science:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
- **Machine Learning:** Decision Tree Classifier (Primary) & Random Forest Classifier (Comparison)
- **Database:** MySQL, `mysql-connector-python`
- **Analytics & BI:** Microsoft Power BI, Microsoft Excel
- **IDE:** VS Code

---

## 3. Project Workflow
```text
Data Generation / Simulation (generate_dataset.py)
                 ↓
Data Cleaning & Anomaly Handling (data_processing.py)
                 ↓
Exploratory Data Analysis & Plots (analysis.py)
                 ↓
Feature Engineering & Encoding
                 ↓
Model Training & Evaluation (train_model.py)
                 ↓
Interactive Web Dashboard & Predictor (app.py)
                 ↓
MySQL Database Integration (database/database.sql)
                 ↓
Power BI Business Intelligence Dashboard
```

---

## 4. Directory Structure
```text
mumbai-commute-analytics/
├── app.py                     # Flask web server & prediction routes
├── analysis.py                # EDA and Seaborn/Matplotlib chart generator
├── data_processing.py         # Data cleaning & anomaly filtering pipeline
├── generate_dataset.py        # Realistic Mumbai commute dataset simulation
├── train_model.py             # Decision Tree & Random Forest training
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── data/
│   ├── commute_data.csv       # Raw simulated dataset (with intentional dirt)
│   └── commute_data_cleaned.csv # Cleaned, standardized dataset
│
├── model/
│   ├── commute_model.pkl      # Trained Decision Tree model bundle
│   └── model_metrics.json     # Accuracy and evaluation reports
│
├── database/
│   ├── database.sql           # MySQL database schema & viva queries
│   └── load_to_mysql.py       # Helper script to load cleaned CSV into MySQL
│
├── powerbi/
│   └── POWERBI_GUIDE.md       # Step-by-step Power BI dashboard guide & DAX
│
├── templates/
│   ├── base.html              # Shared layout & navigation
│   ├── index.html             # Home page
│   ├── dashboard.html         # Key metrics & Chart.js visualizations
│   ├── comparison.html        # Side-by-side mode comparison
│   ├── data.html              # Searchable, filterable records table
│   ├── analytics.html         # Seaborn EDA charts & findings
│   ├── prediction.html        # Interactive ML mode prediction form
│   └── about.html             # Project documentation & Viva prep guide
│
└── static/
    ├── css/
    │   └── style.css          # Custom styling & color schemes
    ├── js/
    │   └── script.js          # Client-side table search & UI helpers
    └── images/                # Generated EDA & ML evaluation charts
        ├── transport_comparison.png
        ├── distance_vs_time_cost.png
        ├── peak_hour_impact.png
        ├── crowd_distribution.png
        ├── route_analysis.png
        ├── confusion_matrix.png
        └── feature_importance.png
```

---

## 5. How to Run the Project (Step-by-Step)

### Step 1: Open VS Code & Open Terminal
Open VS Code in the project directory:
```powershell
cd "D:\mern sanober\mumbai-commute-analytics"
```

### Step 2: Install Required Libraries
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Data Processing Pipeline
Clean the raw dataset (removes duplicates, imputes missing values, removes invalid numbers):
```powershell
python data_processing.py
```

### Step 4: Run Exploratory Data Analysis (EDA)
Generate all statistical summary charts in `static/images/`:
```powershell
python analysis.py
```

### Step 5: Train the Machine Learning Model
Train Decision Tree & Random Forest classifiers, evaluate accuracy, and save the model:
```powershell
python train_model.py
```

### Step 6: Start the Flask Web Application
```powershell
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 6. Machine Learning Model Performance
- **Primary Model:** Decision Tree Classifier (`max_depth=5`)
- **Comparison Model:** Random Forest Classifier (`n_estimators=100`)
- **Accuracy:** **~97.1%** on unseen test data
- **Primary Influencing Features:** Travel Cost, Travel Time, Distance, Crowd Level, Delay.

