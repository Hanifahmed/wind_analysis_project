
Wind Capacity Factor Analysis (Germany, Denmark, Netherlands)
---

This project analyzes hourly wind capacity factor (CF) data for Germany (DE), Denmark (DK), and the Netherlands (NL) using 2024 ERA5/ECMWF-based country-level time series.

The workflow evaluates variability, persistence, reliability thresholds, ramp behavior, seasonal structure, duration curves, and normalized annual energy production.

Features
---

Preprocessing
- Reads ERA5/ECMWF CSV input and skips metadata rows
- Cleans and prepares hourly, time-indexed CF datasets

Exploratory Analysis
- Hourly comparison plots
- Daily, weekly, and monthly aggregation
- Histograms, boxplots, and diurnal patterns
- Monthly and seasonal capacity factor analysis

Reliability and Persistence
- Quantifies low-CF and high-CF hours
- Calculates longest consecutive low/high CF events
- Evaluates threshold reliability for CF levels of 0.1, 0.2, 0.3, and 0.4

Variability and Ramping
- Computes coefficient of variation
- Computes mean absolute ramp, 95th percentile ramp, and maximum upward/downward ramps

Energy Metric
- Estimates annual energy production normalized to 1 MW installed capacity

Usage
- Place the dataset in the data/ folder
- Update the DATA_FILE path in src/wind_capacity_analysis.py if needed
- Run:
  python src/wind_capacity_analysis.py  - Evaluates probabilities across thresholds `[0.1, 0.2, 0.3, 0.4]`.
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
