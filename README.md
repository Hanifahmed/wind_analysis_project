# Wind Analysis Project

## Project Overview
This project performs a **preliminary wind resource assessment** using ERA5 reanalysis data.  
It calculates key wind statistics, wind power density, turbine mean power, annual energy production (AEP), and capacity factors for different hub heights and turbine models.

The project is designed for **industry applications**, allowing quick assessment of potential wind sites.


## Data Source
- ERA5 Reanalysis Data (10m & 100m wind components, temperature, pressure)
- Time period: [Specify your range, e.g., 2023-01-01 to 2023-12-31]
- Variables used: `wind_speed_10m`, `u10`, `v10`, `temp_2m`, `msl_pressure`


## Project Structure


## Analysis Workflow

1. **Data Preprocessing**
   - Extract wind speed from ERA5 data
   - Compute magnitude from `u10` and `v10`
   - Clean missing values

2. **Wind Statistics**
   - Mean, min, max wind speed
   - Histogram and Weibull fit
   - Weibull parameters: shape `k`, scale `c`

3. **Wind Power Analysis**
   - Wind Power Density (W/m²)
   - Mean power per turbine (kW)
   - Annual Energy Production (MWh)
   - Capacity Factor (%)
   - Comparison of different hub heights & turbine models

4. **Visualization**
   - Wind speed histogram
   - Weibull distribution plot
   - Optional: wind rose

5. **Reporting**
   - Summary report with key results
   - Recommendations for turbine selection & hub height


## How to Run
1. Open `notebooks/wind_analysis.ipynb` in Google Colab.
2. Install required packages:
   ```python
   !pip install numpy pandas matplotlib scipy xarray windrose