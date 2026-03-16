---
title: "USD/PHP FX Risk Analysis | Items 1-6"
output: 
  html_document:
    df_print: kable
---



# Section 1: Data Load and Integrity Check


Table: Data Integrity Check

|Metric               |Value      |
|:--------------------|:----------|
|Total Row Count      |1736       |
|Start Date           |2019-01-02 |
|End Date             |2026-02-27 |
|Rows with High < Low |3          |

# Section 2: Data Cleaning



# Section 3: Window Definitions


Table: Analysis Windows (Return Series)

|     |Window |Start_Date |    n|
|:----|:------|:----------|----:|
|Full |Full   |2019-01-03 | 1735|
|w60  |w60    |2025-11-27 |   60|
|w40  |w40    |2026-01-02 |   40|
|w20  |w20    |2026-01-30 |   20|

# Section 4: Item 1 Tables (DoD VaR 95%)


Table: Item 1: Close-to-Close VaR at 95%

|       |Window |    n|    VaR_Pct| VaR_Cents|
|:------|:------|----:|----------:|---------:|
|5%...1 |Full   | 1735| -0.5247701|   -28.620|
|5%...2 |w60    |   60| -0.4781771|   -28.200|
|5%...3 |w40    |   40| -0.4802720|   -28.325|
|5%...4 |w20    |   20| -0.5005179|   -29.475|



Table: Item 1: Outliers (0.1% / 99.9% Bounds)

|Date       | Close|   dod_pct| dod_cents|
|:----------|-----:|---------:|---------:|
|2022-11-11 | 57.23| -1.649768|       -96|
|2022-12-27 | 55.90|  1.359927|        75|
|2023-02-06 | 54.39|  1.322653|        71|
|2025-01-02 | 57.91| -1.830819|      -108|

# Section 5: Item 2 Tables (Intraday VaR 95%)


Table: Item 2: Intraday VaR at 95% (Right Tail)

|        |Window |    n| VaR_Cents|   VaR_Pct|
|:-------|:------|----:|---------:|---------:|
|95%...1 |Full   | 1736|    40.000| 0.7308963|
|95%...2 |w60    |   60|    29.400| 0.4990832|
|95%...3 |w40    |   40|    29.400| 0.4990832|
|95%...4 |w20    |   20|    37.495| 0.6528108|



Table: Item 2: Outliers (99.9% Bound)

|Date       |  High|   Low| intraday_cents| intraday_pct|
|:----------|-----:|-----:|--------------:|------------:|
|2019-09-04 | 52.93| 51.92|            101|     1.945301|
|2024-09-12 | 56.20| 55.08|            112|     2.033406|

# Section 6: Item 3 Table (Gap Analysis)


Table: Item 3: VaR Gap (Intraday - |DoD|)

|Window | dod_var| intra_var|    Gap|
|:------|-------:|---------:|------:|
|Full   | -28.620|    40.000| 11.380|
|w60    | -28.200|    29.400|  1.200|
|w40    | -28.325|    29.400|  1.075|
|w20    | -29.475|    37.495|  8.020|

# Section 7: Item 4 Table (CVaR & Winsorization)


Table: Item 4: Results (Full History)

|Metric                    | Percentage|     Cents|
|:-------------------------|----------:|---------:|
|Raw VaR (95%)             | -0.5247701| -28.62000|
|CVaR (Expected Shortfall) | -0.7300547| -40.68276|
|Winsorization LB (0.1%)   | -1.5181572|        NA|
|Winsorization UB (99.9%)  |  1.2951393|        NA|
|VaR after Winsorization   | -0.5247701| -28.62000|
|VaR adjustment            |  0.0000000|   0.00000|

# Section 8: Item 5 Tables (Significance)


Table: Item 5: Significance Tests

|      |Window |  n|   KS_Stat|      KS_p| Levene_Stat|  Levene_p|
|:-----|:------|--:|---------:|---------:|-----------:|---------:|
|D...1 |w60    | 60| 0.0970701| 0.6453206|   0.7428470| 0.4576717|
|D...2 |w40    | 40| 0.1098703| 0.7327428|   0.5779930| 0.5633422|
|D...3 |w20    | 20| 0.2060519| 0.3707250|   0.0713991| 0.9430883|



Table: Item 5: Descriptive Statistics

|Window |    n|   Mean_Pct|    SD_Pct|   Skewness|  Kurtosis|
|:------|----:|----------:|---------:|----------:|---------:|
|Full   | 1735|  0.0059584| 0.3366582|  0.0552255| 2.1138480|
|w60    |   60| -0.0332058| 0.2877804| -0.4344704| 0.9081311|
|w40    |   40| -0.0478826| 0.2893865| -0.8464122| 0.9938221|
|w20    |   20| -0.1092397| 0.3147680| -0.9052837| 0.6524471|



Table: Item 5: VaR Comparison

|       |Window |    n|    VaR_Pct| VaR_Cents| Diff_from_Full|
|:------|:------|----:|----------:|---------:|--------------:|
|5%...1 |Full   | 1735| -0.5247701|   -28.620|      0.0000000|
|5%...2 |w60    |   60| -0.4781771|   -28.200|      0.0465930|
|5%...3 |w40    |   40| -0.4802720|   -28.325|      0.0444981|
|5%...4 |w20    |   20| -0.5005179|   -29.475|      0.0242522|

# Section 9: Item 6 Table (Portfolio)


Table: Item 6: Portfolio Loss and Hedge Sizing

|Parameter               |Value             |
|:-----------------------|:-----------------|
|Reference Date Used     |2024-06-28        |
|FX Rate (PHP/USD)       |58.61             |
|VaR at 99% (%)          |-0.7973968877419  |
|USD Position            |1e+07             |
|1-Day Loss (USD)        |79739.68877419    |
|1-Day Loss (PHP)        |4673543.15905528  |
|Target Max Loss (PHP)   |20000             |
|Reduced USD Position    |42794.0843153417  |
|USD to Remove           |9957205.91568466  |
|Upside Return 99% (%)   |0.922379897194709 |
|Upside Full (PHP)       |5406068.57745819  |
|Upside Reduced (PHP)    |23134.7754518265  |
|Upside Sacrificed (PHP) |5382933.80200636  |

# Section 10: Summary Table


Table: Final Summary Table

| Item|Description                 |Result                   |
|----:|:---------------------------|:------------------------|
|    1|Close-to-close VaR 95% full |-28.62 cents / -0.5248 % |
|    1|Outlier count (DoD)         |4                        |
|    2|Intraday VaR 95% full       |40 cents / 0.7309 %      |
|    2|Outlier count (Intraday)    |2                        |
|    3|VaR gap full                |11.38 cents              |
|    4|CVaR 95% full               |-40.68 cents / -0.7301 % |
|    4|Winsorization adjustment    |0.00 cents               |
|    5|KS test p-values (60,40,20) |0.6453, 0.7327, 0.3707   |
|    5|Max VaR diff across windows |0.0466 pp                |
|    6|1-day loss USD 10M (PHP)    |PHP 4,673,543            |
|    6|USD pos to cap at PHP 20K   |USD 42,794.08            |
|    6|Upside sacrificed           |PHP 5,382,934            |
