# Wind Capacity Factor Analysis (Germany, Denmark, Netherlands)

## Overview
This project analyzes hourly wind capacity factor (CF) time series for Germany, Denmark, and the Netherlands using 2024 ERA5/ECMWF-derived country-level data. The workflow focuses on variability, persistence, reliability thresholds, ramp behavior, seasonality, duration curves, and normalized annual energy production.

## Dataset
- Source: ERA5/ECMWF-based hourly wind capacity factor dataset
- Time coverage: 2024
- Countries analyzed:
  - Germany (DE)
  - Denmark (DK)
  - Netherlands (NL)

## Methodology
The analysis includes:

1. Data preprocessing
   - Read CSV after skipping metadata rows
   - Parse timestamps
   - Prepare time-indexed country series

2. Descriptive statistics
   - Mean, standard deviation, percentiles, coefficient of variation

3. Persistence analysis
   - Number of low-CF and high-CF hours
   - Maximum consecutive low/high-CF periods

4. Reliability analysis
   - Probability of exceeding CF thresholds: 0.1, 0.2, 0.3, 0.4
   - Maximum consecutive hours below each threshold

5. Seasonal analysis
   - Monthly mean capacity factor
   - Seasonal mean, standard deviation, coefficient of variation

6. Ramp-rate analysis
   - Mean absolute ramp
   - 95th percentile ramp
   - Maximum upward and downward ramps

7. Duration curve
   - Exceedance probability of hourly capacity factor

8. Normalized energy metric
   - Annual capacity factor
   - Annual energy production normalized to 1 MW installed capacity

## Key Results

### Mean annual capacity factor
- Germany: 0.2288
- Denmark: 0.2554
- Netherlands: 0.2633

### Normalized annual energy production (1 MW basis)
- Germany: 2010.13 MWh
- Denmark: 2243.62 MWh
- Netherlands: 2312.87 MWh

### Main interpretation
- The Netherlands shows the highest mean annual capacity factor and highest normalized annual energy production.
- Denmark also performs strongly, with higher average output than Germany.
- Germany has the lowest mean CF, but also lower short-term variability and ramping than the Netherlands.

### Persistence
- Germany records fewer low-CF and high-CF hours than Denmark and the Netherlands.
- Germany shows the longest continuous high-CF event.
- The Netherlands has stronger high-output occurrence overall, but shorter high-CF persistence than Germany.

### Variability and ramps
- Germany has the smallest mean absolute ramp and lowest 95th percentile ramp.
- The Netherlands has the largest ramp magnitudes, indicating stronger short-term volatility.
- Denmark lies between the two.

### Seasonality
- All three countries peak during winter (DJF).
- Capacity factors weaken substantially in summer (JJA).
- The Netherlands leads in winter mean CF, while Germany drops lowest in summer.

## Repository Structure
- `data/` input dataset
- `src/wind_analysis.py` main script
- `Figures/` saved output figures
- `report/` summary text and reporting material

## How to Run
```bash
python src/wind_analysis.py
