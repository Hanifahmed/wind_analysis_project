Wind Capacity Analysis

This project analyzes hourly wind capacity factor (CF) data for Germany, Denmark, and the Netherlands (2024 ERA5/ECMWF data). The workflow includes preprocessing, descriptive statistics, exploratory analysis, extreme wind detection, reliability analysis, and energy production estimates.

Features

Preprocess raw ERA5/ECMWF CSV data (skips metadata rows).

Analyze Germany, Denmark, and Netherlands wind CF.

Visualizations:

Hourly, daily, weekly, and monthly CF plots.

Histograms and boxplots.

Diurnal and monthly wind patterns.

Extreme wind periods (low/high thresholds).

Reliability bar charts.


Capacity Factor (CF) and Annual Energy Production (AEP) estimates.


Figures

All figures are shown during execution (so you can view results directly in Colab/IDE).

Figures are also saved automatically in the Figures/ folder as PNG files.

Saved with consistent DPI and tight layout for publication quality.


Usage

1. Place your CSV file in the data/ directory and update the DATA_FILE variable in the script if needed.


2. Run the Python script (wind_capacity_analysis.py).


3. Check the Figures/ folder for all generated plots.


4. Console output will display descriptive statistics, summaries, and energy calculations.



Example Output

Germany Annual Capacity Factor

Germany Estimated Annual Energy Production (AEP)

Comparative reliability summaries for DE, DK, NL


Project Structure

wind-energy-analysis/
│── data/                # Input datasets (.csv)
│── Figures/             # Saved plots (.png)
│── notebooks/           # Original Jupyter notebooks (.ipynb)
│── src/                 # Python scripts (.py)
│── README.md            # Project documentation (this file)

Notes

The script uses Matplotlib and Seaborn for visualization.

Reliability thresholds and extreme wind thresholds are configurable.

Rated turbine capacity for AEP is set to 3 MW (modifiable in script).



---

This project is structured for portfolio and GitHub publishing — ready to showcase on LinkedIn.

