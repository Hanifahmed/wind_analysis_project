import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Configuration
# ==============================
DATA_FILE = "data/ERA5_Wind_2024.csv"
FIG_FOLDER = "Figures"
os.makedirs(FIG_FOLDER, exist_ok=True)

# ==============================
# Helper Functions
# ==============================
def preprocess_country(df, country_code):
    """Extract and preprocess data for a given country."""
    if country_code not in df.columns:
        raise ValueError(f"Country code {country_code} not found in CSV")
    data = df[["Date", country_code]].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data[country_code] = pd.to_numeric(data[country_code], errors="coerce")
    data.set_index("Date", inplace=True)
    return data.dropna()

def save_and_show(fig, filename):
    """Show and save figure to Figures/ folder."""
    filepath = os.path.join(FIG_FOLDER, filename)
    plt.show()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")

# ==============================
# Load Data
# ==============================
print("Reading CSV...")
df = pd.read_csv(DATA_FILE, skiprows=52, header=0)
print("Columns available:", df.columns.tolist()[:10])

# Preprocess each country
de_data = preprocess_country(df, "DE")
dk_data = preprocess_country(df, "DK")
nl_data = preprocess_country(df, "NL")
countries = {"DE": de_data, "DK": dk_data, "NL": nl_data}

# ==============================
# Germany - Exploratory Analysis
# ==============================
print("Germany Data Shape:", de_data.shape)

# Hourly plot
fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(de_data.index, de_data["DE"], linewidth=0.5, color="blue")
ax.set_title("Germany (DE) Wind Capacity Factor - Hourly (2024)")
ax.set_xlabel("Date"); ax.set_ylabel("Wind Capacity Factor (MW/MW)")
ax.grid(True)
save_and_show(fig, "DE_hourly.png")

# Aggregates
de_daily = de_data["DE"].resample("D").mean()
de_weekly = de_data["DE"].resample("W-MON").mean()
de_monthly = de_data["DE"].resample("M").mean()

fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(de_daily.index, de_daily, label="Daily", color="orange")
ax.plot(de_weekly.index, de_weekly, label="Weekly", color="green")
ax.plot(de_monthly.index, de_monthly, label="Monthly", color="blue")
ax.legend(); ax.grid(True)
ax.set_title("Germany (DE) Aggregated Wind Capacity Factor")
ax.set_xlabel("Date"); ax.set_ylabel("Wind CF")
save_and_show(fig, "DE_aggregated.png")

# ==============================
# Descriptive Statistics (DE, DK, NL)
# ==============================
for country, data in countries.items():
    print(f"\n{country} Statistics:\n", data[country].describe())

    # Histogram
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data[country], bins=50, kde=True, ax=ax, color="skyblue")
    ax.set_title(f"Histogram of {country} Wind Capacity Factor")
    save_and_show(fig, f"{country}_histogram.png")

    # Boxplot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=data[country], ax=ax, color="lightgreen")
    ax.set_title(f"Boxplot of {country} Wind Capacity Factor")
    save_and_show(fig, f"{country}_boxplot.png")

    # Diurnal
    hourly = data[country].groupby(data.index.hour).mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly.index, hourly.values, marker="o", color="orange")
    ax.set_title(f"Average Hourly Wind Capacity Factor ({country})")
    ax.set_xlabel("Hour of Day"); ax.set_ylabel("Avg Wind CF")
    save_and_show(fig, f"{country}_hourly.png")

    # Monthly
    monthly = data[country].resample("M").mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly.values, marker="o", color="green")
    ax.set_title(f"Monthly Average Wind Capacity Factor ({country})")
    save_and_show(fig, f"{country}_monthly.png")

# ==============================
# Extreme Wind & Reliability Analysis
# ==============================
low_thr, high_thr = 0.035, 0.517
reliability_thresholds = [0.1, 0.2, 0.3, 0.4]

summary = {}
for country, data in countries.items():
    data["Low_Wind"] = data[country] <= low_thr
    data["High_Wind"] = data[country] >= high_thr

    summary[country] = {
        "Low_Wind_Hours": int(data["Low_Wind"].sum()),
        "High_Wind_Hours": int(data["High_Wind"].sum())
    }

summary_df = pd.DataFrame(summary).T
print("\nExtreme Wind Summary:\n", summary_df)

# Reliability Analysis
results = {}
for country, data in countries.items():
    total_hours = len(data)
    res = []
    for thr in reliability_thresholds:
        above = (data[country] >= thr).mean()
        below = 1 - above
        res.append({"Threshold": thr, "P_Above": above, "P_Below": below})
    results[country] = pd.DataFrame(res)

# ==============================
# Germany - Capacity Factor & Power Output
# ==============================
P_rated = 3000  # kW (example rated turbine size)
de_data["Power_kW"] = de_data["DE"] * P_rated

CF = de_data["DE"].mean()
AEP = de_data["Power_kW"].sum() / 1000  # MWh
print(f"\nGermany Annual CF: {CF:.2%}")
print(f"Germany Estimated AEP: {AEP:,.0f} MWh")

monthly_cf = de_data["DE"].resample("M").mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_cf.index, monthly_cf.values, marker="o", color="blue")
ax.set_title("Monthly Capacity Factor (Germany 2024)")
ax.set_xlabel("Month"); ax.set_ylabel("Capacity Factor")
ax.grid(True)
save_and_show(fig, "DE_monthly_CF.png")

print(f"\nAll figures saved in: {FIG_FOLDER}")
