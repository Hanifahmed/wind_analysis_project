# 🌍 Wind Capacity Analysis (Germany, Denmark, Netherlands)

This project analyzes **hourly wind capacity factor (CF)** data for **Germany (DE)**, **Denmark (DK)**, and **the Netherlands (NL)** using **2024 ERA5/ECMWF reanalysis data**.  
It evaluates wind performance, extreme wind events, reliability thresholds, and annual energy production estimates.

---

## 🔑 Features
- **Preprocessing**
  - Reads ERA5/ECMWF CSV (skips metadata rows).
  - Cleans and prepares time-indexed CF datasets.
- **Exploratory Analysis**
  - Hourly, daily, weekly, and monthly CF plots.
  - Histograms, boxplots, diurnal & seasonal patterns.
- **Extreme Wind Analysis**
  - Identifies low-wind and high-wind periods.
  - Calculates consecutive extreme wind durations.
- **Reliability Analysis**
  - Evaluates probabilities across thresholds `[0.1, 0.2, 0.3, 0.4]`.
  - Generates reliability bar charts.
- **Energy Production**
  - Capacity Factor (CF) estimation.
  - Annual Energy Production (AEP) calculation for a 3 MW turbine.

---

## 📊 Figures
- Plots are **shown live** during execution (in Colab/IDE).
- Figures are also **saved automatically** in the `Figures/` folder as `.png`.
- Saved with consistent DPI and tight layout for **publication-ready quality**.

---

## ⚙️ Usage
1. Place your dataset in the `data/` folder.  
   Update the `DATA_FILE` variable in `src/wind_capacity_analysis.py` if needed.  
2. Run the script:
   ```bash
   python src/wind_capacity_analysis.py