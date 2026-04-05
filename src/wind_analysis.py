import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# Configuration
# ==============================

DATA_FILE = "data/H_ERA5_ECMW_T639_WON_NA---_Pecd_NUT0_S202401010000_E202412312300_CFR_TIM_01h_COM_noc_org_30_NA---_ReGrB_PhM04_PECD4.2_fv1.csv"
FIG_FOLDER = "Figures"
COUNTRIES = ["DE", "DK", "NL"]
COUNTRY_NAMES = {
    "DE": "Germany",
    "DK": "Denmark",
    "NL": "Netherlands",
}

LOW_CF_THRESHOLD = 0.05
HIGH_CF_THRESHOLD = 0.50
RELIABILITY_THRESHOLDS = [0.1, 0.2, 0.3, 0.4]
NORMALIZED_INSTALLED_CAPACITY_MW = 1.0  # normalized AEP basis

os.makedirs(FIG_FOLDER, exist_ok=True)

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True


# ==============================
# Utility functions
# ==============================

def save_and_show(fig, filename: str) -> None:
    path = os.path.join(FIG_FOLDER, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def prepare_country_data(df: pd.DataFrame, country_code: str) -> pd.DataFrame:
    data = df[["Date", country_code]].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data[country_code] = pd.to_numeric(data[country_code], errors="coerce")
    data = data.dropna(subset=["Date"]).set_index("Date").sort_index()
    return data


def basic_cf_stats(data: pd.DataFrame, col: str) -> pd.Series:
    s = data[col]
    return pd.Series({
        "count": s.count(),
        "mean_cf": s.mean(),
        "std_cf": s.std(),
        "min_cf": s.min(),
        "p10": s.quantile(0.10),
        "p25": s.quantile(0.25),
        "median_cf": s.quantile(0.50),
        "p75": s.quantile(0.75),
        "p90": s.quantile(0.90),
        "max_cf": s.max(),
        "cv_percent": (s.std() / s.mean()) * 100 if s.mean() > 0 else np.nan,
    })


def max_consecutive(flag_series: pd.Series) -> int:
    groups = (flag_series != flag_series.shift()).cumsum()
    return int(flag_series.groupby(groups).sum().max())


def persistence_stats(data: pd.DataFrame, col: str,
                      low_thr: float = LOW_CF_THRESHOLD,
                      high_thr: float = HIGH_CF_THRESHOLD) -> pd.Series:
    s = data[col]
    low_flag = s <= low_thr
    high_flag = s >= high_thr

    return pd.Series({
        "low_cf_hours": int(low_flag.sum()),
        "high_cf_hours": int(high_flag.sum()),
        "max_consec_low_hours": max_consecutive(low_flag),
        "max_consec_high_hours": max_consecutive(high_flag),
    })


def reliability_analysis(series: pd.Series,
                         thresholds=RELIABILITY_THRESHOLDS) -> pd.DataFrame:
    rows = []
    for thr in thresholds:
        above_prob = (series >= thr).mean()
        below_flag = series < thr
        groups = (below_flag != below_flag.shift()).cumsum()
        max_consec_below = int(below_flag.groupby(groups).sum().max())
        rows.append({
            "Threshold": thr,
            "P(CF >= Threshold)": above_prob,
            "P(CF < Threshold)": 1 - above_prob,
            "Max_Consec_Below": max_consec_below,
        })
    return pd.DataFrame(rows)


def monthly_seasonality(data: pd.DataFrame, col: str):
    s = data[col]
    month_mean = s.groupby(s.index.month).mean()
    month_std = s.groupby(s.index.month).std()
    return month_mean, month_std


def seasonal_stats(data: pd.DataFrame, col: str) -> pd.DataFrame:
    s = data[col].copy()
    season_map = {
        12: "DJF", 1: "DJF", 2: "DJF",
        3: "MAM", 4: "MAM", 5: "MAM",
        6: "JJA", 7: "JJA", 8: "JJA",
        9: "SON", 10: "SON", 11: "SON"
    }
    seasons = s.index.month.map(season_map)
    grouped = s.groupby(seasons)
    return pd.DataFrame({
        "mean_cf": grouped.mean(),
        "std_cf": grouped.std(),
        "cv_percent": grouped.std() / grouped.mean() * 100,
    })


def ramp_rate_stats(data: pd.DataFrame, col: str) -> pd.Series:
    s = data[col]
    ramp = s.diff().dropna()
    return pd.Series({
        "mean_abs_ramp": ramp.abs().mean(),
        "p95_abs_ramp": ramp.abs().quantile(0.95),
        "max_up_ramp": ramp.max(),
        "max_down_ramp": ramp.min(),
    })


def annual_energy_from_cf(data: pd.DataFrame, col: str,
                          installed_capacity_mw: float = NORMALIZED_INSTALLED_CAPACITY_MW):
    s = data[col]
    annual_cf = s.mean()
    aep_mwh = (s * installed_capacity_mw).sum()  # hourly data => MW*h = MWh
    return annual_cf, aep_mwh


# ==============================
# Plot functions
# ==============================

def plot_hourly_comparison(countries: dict) -> None:
    fig, ax = plt.subplots(figsize=(15, 4))
    for code, data in countries.items():
        ax.plot(data.index, data[code], label=COUNTRY_NAMES[code], linewidth=0.5, alpha=0.8)
    ax.set_title("Hourly Wind Capacity Factor Comparison (2024)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Capacity Factor")
    ax.legend()
    save_and_show(fig, "hourly_cf_comparison_2024.png")


def plot_aggregated_country(data: pd.DataFrame, col: str, country_name: str) -> None:
    daily = data[col].resample("D").mean()
    weekly = data[col].resample("W-MON").mean()
    monthly = data[col].resample("ME").mean()

    fig, ax = plt.subplots(figsize=(15, 4))
    ax.plot(daily.index, daily.values, label="Daily", alpha=0.6)
    ax.plot(weekly.index, weekly.values, label="Weekly", linewidth=2)
    ax.plot(monthly.index, monthly.values, label="Monthly", linewidth=2)
    ax.set_title(f"{country_name} Wind Capacity Factor Aggregation")
    ax.set_xlabel("Date")
    ax.set_ylabel("Capacity Factor")
    ax.legend()
    save_and_show(fig, f"{country_name}_cf_aggregation.png")


def plot_distribution_and_diurnal(data: pd.DataFrame, col: str, country_name: str) -> None:
    s = data[col]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    axes[0].hist(s.dropna(), bins=50)
    axes[0].set_title(f"{country_name} CF Distribution")
    axes[0].set_xlabel("Capacity Factor")

    axes[1].boxplot(s.dropna(), vert=False)
    axes[1].set_title(f"{country_name} CF Boxplot")
    axes[1].set_xlabel("Capacity Factor")

    diurnal = s.groupby(s.index.hour).mean()
    axes[2].plot(diurnal.index, diurnal.values, marker="o")
    axes[2].set_title(f"{country_name} Mean Diurnal Cycle")
    axes[2].set_xlabel("Hour")
    axes[2].set_ylabel("Capacity Factor")

    save_and_show(fig, f"{country_name}_distribution_diurnal.png")


def plot_monthly_comparison(countries: dict) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    for code, data in countries.items():
        mmean, _ = monthly_seasonality(data, code)
        ax.plot(mmean.index, mmean.values, marker="o", label=COUNTRY_NAMES[code])
    ax.set_title("Monthly Mean Capacity Factor")
    ax.set_xlabel("Month")
    ax.set_ylabel("Capacity Factor")
    ax.set_xticks(range(1, 13))
    ax.legend()
    save_and_show(fig, "monthly_mean_cf_comparison.png")


def plot_duration_curve(data: pd.DataFrame, col: str, country_name: str) -> None:
    s = data[col].dropna().sort_values(ascending=False).reset_index(drop=True)
    exceedance = np.arange(1, len(s) + 1) / len(s) * 100

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(exceedance, s)
    ax.set_xlabel("Exceedance Probability (%)")
    ax.set_ylabel("Capacity Factor")
    ax.set_title(f"{country_name} Capacity Factor Duration Curve")
    save_and_show(fig, f"{country_name}_duration_curve.png")


def plot_mean_cf_bar(final_summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(final_summary.index, final_summary["mean_cf"])
    ax.set_title("Mean Capacity Factor by Country")
    ax.set_ylabel("Capacity Factor")
    save_and_show(fig, "mean_cf_by_country.png")


# ==============================
# Main workflow
# ==============================

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE, skiprows=52)
    print("Columns available:", df.columns.tolist()[:20])
    print("Dataset shape:", df.shape)

    # Prepare country datasets
    countries = {code: prepare_country_data(df, code) for code in COUNTRIES}

    print("\nPrepared datasets:")
    for code, data in countries.items():
        print(f"{COUNTRY_NAMES[code]}: {data.shape}")

    # Basic stats
    summary = pd.DataFrame({
        COUNTRY_NAMES[code]: basic_cf_stats(data, code)
        for code, data in countries.items()
    }).T

    print("\nBasic CF Statistics:")
    print(summary.round(6))

    # Persistence
    persistence = pd.DataFrame({
        COUNTRY_NAMES[code]: persistence_stats(data, code)
        for code, data in countries.items()
    }).T

    print("\nPersistence Statistics:")
    print(persistence)

    # Reliability
    reliability_tables = {}
    for code, data in countries.items():
        rel = reliability_analysis(data[code])
        reliability_tables[COUNTRY_NAMES[code]] = rel
        print(f"\nReliability Analysis — {COUNTRY_NAMES[code]}")
        print(rel.round(6))

    # Seasonal stats
    for code, data in countries.items():
        print(f"\nSeasonal Statistics — {COUNTRY_NAMES[code]}")
        print(seasonal_stats(data, code).round(6))

    # Ramp stats
    ramps = pd.DataFrame({
        COUNTRY_NAMES[code]: ramp_rate_stats(data, code)
        for code, data in countries.items()
    }).T

    print("\nRamp-Rate Statistics:")
    print(ramps.round(6))

    # Normalized annual energy
    energy_rows = []
    for code, data in countries.items():
        annual_cf, aep_mwh = annual_energy_from_cf(data, code)
        energy_rows.append([COUNTRY_NAMES[code], annual_cf, aep_mwh])

    energy_df = pd.DataFrame(
        energy_rows,
        columns=["Country", "Annual_CF", "AEP_MWh_for_1MW"]
    )

    print("\nNormalized Annual Energy:")
    print(energy_df.round(6))

    # Final summary
    final_summary = summary.join(persistence).join(ramps)
    final_summary = final_summary.join(
        energy_df.set_index("Country")[["Annual_CF", "AEP_MWh_for_1MW"]]
    )

    print("\nFinal Summary Table:")
    print(final_summary.round(6))

    # Plots
    plot_hourly_comparison(countries)
    plot_aggregated_country(countries["DE"], "DE", "Germany")
    plot_distribution_and_diurnal(countries["DE"], "DE", "Germany")
    plot_monthly_comparison(countries)
    plot_duration_curve(countries["DE"], "DE", "Germany")
    plot_mean_cf_bar(final_summary)

    print(f"\nAll figures saved in: {FIG_FOLDER}")


if __name__ == "__main__":
    main()
