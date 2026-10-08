# Power BI Dashboard Guide: Mumbai Commute Analytics
**B.Sc Data Science College Project**

This document provides complete step-by-step instructions to create an interactive Power BI dashboard using the cleaned dataset: `data/commute_data_cleaned.csv`.

---

## 1. Connecting Power BI to the Cleaned Dataset
1. Open **Microsoft Power BI Desktop**.
2. Click on **Get Data** (top ribbon) → Select **Text/CSV** → Click **Connect**.
3. Browse and select:
   ```text
   D:\mern sanober\mumbai-commute-analytics\data\commute_data_cleaned.csv
   ```
4. In the preview window, confirm delimiter is **Comma (,)**, then click **Load**.

---

## 2. Calculated DAX Measures (Copy & Paste)
In the Power BI right pane, right-click on the `commute_data_cleaned` table and select **New Measure** to create the following DAX calculations:

### Measure 1: Total Commutes
```dax
Total Commutes = COUNT(commute_data_cleaned[Commute_ID])
```

### Measure 2: Average Travel Time (min)
```dax
Avg Travel Time = ROUND(AVERAGE(commute_data_cleaned[Travel_Time_min]), 1)
```

### Measure 3: Average Cost (INR)
```dax
Avg Cost = ROUND(AVERAGE(commute_data_cleaned[Cost_INR]), 1)
```

### Measure 4: Average Commute Distance (km)
```dax
Avg Distance = ROUND(AVERAGE(commute_data_cleaned[Distance_km]), 1)
```

### Measure 5: Average Cost per Kilometre
```dax
Avg Cost Per Km = ROUND(AVERAGE(commute_data_cleaned[Cost_Per_Km]), 2)
```

---

## 3. Creating the 4 KPI Cards
1. From the **Visualizations** pane, select **Card** (the icon with `123`).
2. Drag `Total Commutes` measure into the **Fields** area. Title: *"Total Trips"*.
3. Add a second **Card** visual → Drag `Avg Travel Time` measure. Title: *"Avg Travel Time (min)"*.
4. Add a third **Card** visual → Drag `Avg Cost` measure. Title: *"Avg Fare Cost (₹)"*.
5. Add a fourth **Card** visual → Drag `Avg Distance` measure. Title: *"Avg Distance (km)"*.

---

## 4. Visualizations & Charts Layout

### Chart 1: Transport Mode Usage Share
- **Visual Type**: **Donut Chart**
- **Legend**: `Transport_Mode`
- **Values**: `Total Commutes` (or Count of `Commute_ID`)
- **Insight**: Displays distribution of trips across Local, Metro, and Auto.

### Chart 2: Average Cost by Transport Mode
- **Visual Type**: **Clustered Column Chart**
- **X-axis**: `Transport_Mode`
- **Y-axis**: `Avg Cost`
- **Insight**: Shows Auto is highest in fare cost, Local is cheapest.

### Chart 3: Travel Time — Peak vs Off-Peak Hour
- **Visual Type**: **Clustered Bar Chart**
- **Y-axis**: `Transport_Mode`
- **X-axis**: `Travel_Time_min` (Average)
- **Legend**: `Peak_Hour`
- **Insight**: Highlights how Auto travel time surges during peak rush due to street traffic.

### Chart 4: Crowd Level Distribution across Modes
- **Visual Type**: **100% Stacked Bar Chart**
- **Y-axis**: `Transport_Mode`
- **X-axis**: Count of `Commute_ID`
- **Legend**: `Crowd_Level`
- **Insight**: Visualizes super-dense crowding in Local trains vs low crowd in Auto.

### Chart 5: Distance vs Travel Time Scatter
- **Visual Type**: **Scatter Chart**
- **X-axis**: `Distance_km`
- **Y-axis**: `Travel_Time_min`
- **Legend**: `Transport_Mode`
- **Insight**: Shows high variance for Auto at higher distances, consistent linear travel times for Metro.

---

## 5. Adding Interactive Slicers (Filters)
Add the following **Slicer** visuals at the top or left pane for user interactivity:
1. **Slicer 1**: `Transport_Mode` (Tiles or Dropdown: Metro, Local, Auto)
2. **Slicer 2**: `Peak_Hour` (Yes / No)
3. **Slicer 3**: `Weather` (Clear, Overcast, Rainy)
4. **Slicer 4**: `Starting_Area` (Dropdown)

---

## 6. Academic Disclaimer Card (Mandatory)
Insert a **Text Box** at the bottom of the canvas:
> *"This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics."*

