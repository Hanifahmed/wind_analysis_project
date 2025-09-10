# wind_analysis.py
# GitHub-ready Python script for Wind Energy Analysis (DE, DK, NL)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# 1. Load and preprocess data
# -----------------------------
def load_country_data(filename, country_code):
    df = pd.read_csv(filename, skiprows=52, header=0)
    data = df[['Date', country_code]].copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data[country_code] = pd.to_numeric(data[country_code], errors='coerce')
    data.set_index('Date', inplace=True)
    return data

# -----------------------------
# 2. Descriptive statistics & plots
# -----------------------------
def descriptive_stats(data, country_code):
    print(f"\n--- {country_code} Wind Capacity Factor Statistics ---")
    print(data[country_code].describe())
    
    # Histogram
    plt.figure(figsize=(10,5))
    sns.histplot(data[country_code], bins=50, kde=True, color='skyblue')
    plt.title(f"Histogram of {country_code} Wind Capacity Factor")
    plt.xlabel("Wind Capacity Factor")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Boxplot
    plt.figure(figsize=(8,4))
    sns.boxplot(x=data[country_code], color='lightgreen')
    plt.title(f"Boxplot of {country_code} Wind Capacity Factor")
    plt.xlabel("Wind Capacity Factor")
    plt.tight_layout()
    plt.show()
    
    # Diurnal pattern
    hourly_avg = data[country_code].groupby(data.index.hour).mean()
    plt.figure(figsize=(10,5))
    plt.plot(hourly_avg.index, hourly_avg.values, marker='o', color='orange')
    plt.title(f"Average Hourly Wind Capacity Factor ({country_code})")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Wind Capacity Factor")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Monthly pattern
    monthly_avg = data[country_code].resample('M').mean()
    plt.figure(figsize=(10,5))
    plt.plot(monthly_avg.index, monthly_avg.values, marker='o', color='green')
    plt.title(f"Monthly Average Wind Capacity Factor ({country_code})")
    plt.xlabel("Month")
    plt.ylabel("Average Wind Capacity Factor")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -----------------------------
# 3. Extreme wind analysis
# -----------------------------
def extreme_wind_analysis(data, country_code, low_thr=0.035, high_thr=0.517):
    data['Low_Wind'] = data[country_code] <= low_thr
    data['High_Wind'] = data[country_code] >= high_thr

    # Max consecutive low/high wind hours
    data['Low_Group'] = (data['Low_Wind'] != data['Low_Wind'].shift()).cumsum()
    low_periods = data.groupby('Low_Group').apply(lambda x: len(x) if x['Low_Wind'].iloc[0] else 0)
    max_low_consec = low_periods[low_periods>0].max() if not low_periods.empty else 0

    data['High_Group'] = (data['High_Wind'] != data['High_Wind'].shift()).cumsum()
    high_periods = data.groupby('High_Group').apply(lambda x: len(x) if x['High_Wind'].iloc[0] else 0)
    max_high_consec = high_periods[high_periods>0].max() if not high_periods.empty else 0

    summary = {
        "Low_Wind_Hours": data['Low_Wind'].sum(),
        "High_Wind_Hours": data['High_Wind'].sum(),
        "Max_Consec_Low": max_low_consec,
        "Max_Consec_High": max_high_consec
    }
    print(f"\nExtreme Wind Summary ({country_code}): {summary}")
    return summary

# -----------------------------
# 4. Reliability analysis
# -----------------------------
def reliability_analysis(data_column, thresholds=[0.1,0.2,0.3,0.4]):
    total_hours = len(data_column)
    results = []
    for thr in thresholds:
        above = (data_column >= thr).sum() / total_hours
        below = (data_column < thr).sum() / total_hours
        # Max consecutive hours below threshold
        condition = data_column < thr
        groups = (condition != condition.shift()).cumsum()
        consecutive = data_column.groupby(groups).apply(lambda x: len(x) if x.iloc[0] < thr else 0)
        max_consec = consecutive.max() if len(consecutive)>0 else 0
        results.append({
            "Threshold": thr,
            "Probability_Above": above,
            "Probability_Below": below,
            "Max_Consec_Below": max_consec
        })
    return pd.DataFrame(results)

# -----------------------------
# 5. Capacity Factor & Power Output
# -----------------------------
def calculate_power_output(data, country_code, P_rated=3000):
    df = data.copy()
    df['Power_kW'] = df[country_code] * P_rated
    CF = df[country_code].mean()
    monthly_cf = df[country_code].resample('ME').mean()
    AEP = df['Power_kW'].sum() / 1000  # MWh
    print(f"\n{country_code} - Annual CF: {CF:.2%}, AEP: {AEP:,.0f} MWh")
    return df, CF, monthly_cf, AEP

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    # Path to CSV (update if using local folder or GitHub raw CSV)
    filename = "data/ERA5_Wind_2024.csv"

    # Load datasets
    de_data = load_country_data(filename, "DE")
    dk_data = load_country_data(filename, "DK")
    nl_data = load_country_data(filename, "NL")

    # Descriptive stats & plots
    for country, data in zip(['DE','DK','NL'], [de_data, dk_data, nl_data]):
        descriptive_stats(data, country)

    # Extreme wind analysis
    extreme_summary = {}
    for country, data in zip(['DE','DK','NL'], [de_data, dk_data, nl_data]):
        extreme_summary[country] = extreme_wind_analysis(data, country)

    # Reliability analysis
    reliability_results = {}
    for country, data in zip(['DE','DK','NL'], [de_data, dk_data, nl_data]):
        reliability_results[country] = reliability_analysis(data[country])
        print(f"\nReliability Results ({country}):\n", reliability_results[country])

    # Capacity factor & power
    for country, data in zip(['DE','DK','NL'], [de_data, dk_data, nl_data]):
        df_power, CF, monthly_cf, AEP = calculate_power_output(data, country)
