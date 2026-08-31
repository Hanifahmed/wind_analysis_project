# Wind Power Capacity Factor Analysis — Germany 2024

## Overview

This project is a first pilot analysis of wind power data using an ERA5-derived dataset from the Pan-European Climate Database (PECD).

The analysis focuses on Germany during 2024 and investigates the temporal variability of wind power capacity factor using Python.

The project was developed as an introductory exercise in applying meteorological data analysis to wind energy.

## Objectives

The main objectives are to:

* Load and inspect a real wind-energy dataset
* Calculate basic statistics of wind power capacity factor
* Examine the hourly capacity-factor distribution
* Analyse monthly variability
* Compare seasonal capacity factors
* Create a capacity-factor duration curve
* Estimate annual energy production for an example installed capacity

## Dataset

The data are derived from the ERA5 reanalysis dataset and provided through the Pan-European Climate Database (PECD).

The original CSV contains hourly wind-power capacity-factor data for multiple countries.

For this project, the `DE` column is used for Germany.

### Data characteristics

| Property               | Description                |
| ---------------------- | -------------------------- |
| Region                 | Germany                    |
| Year                   | 2024                       |
| Temporal resolution    | Hourly                     |
| Number of observations | 8,784                      |
| Main variable          | Wind power capacity factor |
| Source                 | ERA5-derived PECD data     |

2024 is a leap year, so the expected number of hourly observations is:

$$
366 \times 24 = 8,784
$$

## Capacity Factor

Capacity factor describes the ratio between actual power production and the rated power of a wind turbine or wind farm:

$$
CF = \frac{P_{actual}}{P_{rated}}
$$

For example:

$$
CF = 0.54 = 54\%
$$

The values in the `DE` column therefore represent capacity factor and **not wind speed in m/s**.

## Methodology

The analysis follows a simple Python workflow:

1. Load the PECD CSV file
2. Skip the metadata section of the CSV
3. Parse the country-level data
4. Select Germany (`DE`)
5. Convert the date column to datetime
6. Convert capacity-factor values to numeric values
7. Calculate descriptive statistics
8. Calculate the annual mean capacity factor
9. Analyse monthly and seasonal variability
10. Plot the capacity-factor distribution
11. Create a capacity-factor duration curve
12. Estimate annual energy production for an example installed capacity

## Results

The notebook produces several visualisations:

* Hourly capacity-factor distribution
* Monthly average capacity factor
* Seasonal average capacity factor
* Capacity-factor duration curve

The project also calculates the annual mean capacity factor and provides a simple example of annual energy production based on an assumed installed capacity.

## Important Limitations

This project uses an ERA5-derived PECD capacity-factor dataset rather than measured wind-farm SCADA data.

Therefore, the results should **not** be interpreted as:

* a bankable wind-resource assessment,
* measured wind-farm production,
* or a detailed site-specific turbine assessment.

The capacity factor has already been derived using the PECD wind-power modelling methodology. This project therefore analyses the resulting capacity-factor time series rather than independently calculating turbine power from raw wind-speed data.

## Tools

The project uses basic Python data-analysis libraries:

* Python
* Pandas
* NumPy
* Matplotlib
* Google Colab

## Project Structure

```text
wind_analysis_project/
│
├── data/
│   └── ERA5_Wind_2024.csv
│
├── notebooks/
│   └── wind_capacity_factor_analysis.ipynb
│
├── figures/
│   ├── capacity_factor_distribution.png
│   ├── monthly_capacity_factor.png
│   ├── seasonal_capacity_factor.png
│   └── capacity_factor_duration_curve.png
│
├── README.md
│
└── requirements.txt
```

## How to Run

The analysis was developed in Google Colab.

Open the notebook and run the cells from top to bottom.

The notebook loads the dataset directly from this GitHub repository, so the CSV does not need to be downloaded manually.

## Data Source

The dataset is based on ERA5 reanalysis and is distributed through the Pan-European Climate Database (PECD).

Reference:

Copernicus Climate Change Service / ECMWF, *Climate and energy related variables from the Pan-European Climate Database (PECD) derived from reanalysis and climate projections, v4.2 Product User Guide*.

## Future Improvements

Possible extensions of this pilot project include:

* Analysis of multiple years
* Comparison of Germany with other countries
* Spatial analysis of wind resources
* Analysis using raw ERA5 wind-speed components
* Wind-speed distribution and Weibull analysis using appropriate wind-speed data
* Analysis at different hub heights
* Comparison with measured wind-energy data
* More detailed wind-resource assessment

## Author

Hanif Ahmed

M.Sc. Marine Geoscience
University of Bremen

Interests: Climate Data Analysis, Meteorology, Wind Energy and Renewable Energy
