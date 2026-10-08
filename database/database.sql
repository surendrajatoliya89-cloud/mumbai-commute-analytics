-- ==========================================================
-- Mumbai Commute Analytics — MySQL Database Setup & Queries
-- Academic College Project (B.Sc Data Science)
-- ==========================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS mumbai_commute_db;
USE mumbai_commute_db;

-- 2. Create Table for Cleaned Commute Records
DROP TABLE IF EXISTS commute_data;

CREATE TABLE commute_data (
    Commute_ID VARCHAR(20) PRIMARY KEY,
    Date DATE NOT NULL,
    Starting_Area VARCHAR(50) NOT NULL,
    Destination VARCHAR(50) NOT NULL,
    Transport_Mode VARCHAR(20) NOT NULL,
    Distance_km DECIMAL(5,2) NOT NULL,
    Travel_Time_min INT NOT NULL,
    Waiting_Time_min INT NOT NULL,
    Cost_INR INT NOT NULL,
    Peak_Hour VARCHAR(5) NOT NULL,
    Crowd_Level VARCHAR(20) NOT NULL,
    Delay_min INT NOT NULL,
    Weather VARCHAR(20) NOT NULL,
    Comfort_Rating INT NOT NULL,
    User_Rating INT NOT NULL,
    Total_Trip_Time_min INT,
    Cost_Per_Km DECIMAL(6,2),
    Speed_kmh DECIMAL(5,2)
);

-- ==========================================================
-- BEGINNER-FRIENDLY COLLEGE VIVA SQL QUERIES
-- ==========================================================

-- Query 1: Average Cost by Transport Mode
-- Objective: Identifies the most and least expensive modes of travel.
SELECT 
    Transport_Mode,
    COUNT(*) AS Total_Trips,
    ROUND(AVG(Cost_INR), 2) AS Avg_Cost_INR,
    ROUND(AVG(Cost_Per_Km), 2) AS Avg_Cost_Per_Km
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_Cost_INR ASC;

-- Query 2: Average Travel Time by Transport Mode
-- Objective: Measures operational travel duration across modes.
SELECT 
    Transport_Mode,
    ROUND(AVG(Travel_Time_min), 2) AS Avg_Travel_Time_min,
    ROUND(AVG(Waiting_Time_min), 2) AS Avg_Waiting_Time_min,
    ROUND(AVG(Delay_min), 2) AS Avg_Delay_min
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Avg_Travel_Time_min ASC;

-- Query 3: Most-Used Transport Mode
-- Objective: Evaluates mode preference in the dataset.
SELECT 
    Transport_Mode,
    COUNT(*) AS Trip_Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM commute_data), 2) AS Percentage_Share
FROM commute_data
GROUP BY Transport_Mode
ORDER BY Trip_Count DESC;

-- Query 4: Peak-Hour Effect on Travel Time
-- Objective: Measures traffic bottleneck impact on peak vs off-peak commutes.
SELECT 
    Transport_Mode,
    Peak_Hour,
    ROUND(AVG(Travel_Time_min), 2) AS Avg_Travel_Time_min,
    ROUND(AVG(Delay_min), 2) AS Avg_Traffic_Delay_min
FROM commute_data
GROUP BY Transport_Mode, Peak_Hour
ORDER BY Transport_Mode, Peak_Hour DESC;

-- Query 5: Crowd Severity Distribution Across Modes
-- Objective: Quantifies passenger congestion levels.
SELECT 
    Transport_Mode,
    Crowd_Level,
    COUNT(*) AS Commute_Count
FROM commute_data
GROUP BY Transport_Mode, Crowd_Level
ORDER BY Transport_Mode, Commute_Count DESC;

-- Query 6: Area-Wise Commute Travel Time & Cost
-- Objective: Identifies high-friction suburban routes.
SELECT 
    Starting_Area,
    Destination,
    COUNT(*) AS Trips,
    ROUND(AVG(Distance_km), 1) AS Avg_Distance_km,
    ROUND(AVG(Travel_Time_min), 1) AS Avg_Time_min,
    ROUND(AVG(Cost_INR), 1) AS Avg_Cost_INR
FROM commute_data
GROUP BY Starting_Area, Destination
HAVING Trips >= 5
ORDER BY Avg_Time_min DESC
LIMIT 10;

