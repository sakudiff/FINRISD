# USD/PHP FX Risk Analysis — 10-Slide Presentation Plan

**Audience:** Prof. Bismark, FINRISD Section C02  
**Constraint:** Maximum 10 slides for submission (appendices excluded from count)  
**Source:** All figures from `fx_analysis.Rmd` — use inline R variables for live numbers  

---

## Slide 1 — Title & Executive Summary

**Visual:** Full price history chart (`price_history_viz`) — 7-year USD/PHP with shaded stress regimes  
**Key Figures:**
- Data span: `r format(min(df$Date), "%d %b %Y")` – `r format(max(df$Date), "%d %b %Y")` (`r nrow(df_returns)` trading days)
- Full-history DoD VaR 95%: `r round(item1_var$VaR_Pct[item1_var$Window == "Full"], 4)`%
- Intraday VaR 95%: `r round(item2_var$VaR_Pct[item2_var$Window == "Full"], 4)`%

**Talking Points:**
- Close-to-close VaR systematically understates risk vs. intraday reality
- Short windows (20/40/60 days) suffer from recency bias — exclude 2020 COVID and 2022 depreciation stress regimes
- CVaR (Expected Shortfall) is the coherent alternative; translation invariance sizes the hedge
- Group members: Antiado, Bolanos, Patajo, Siapno, Sison, Uy

---

## Slide 2 — Item 1: Close-to-Close VaR (95%, One-Tail)

**Visual:** Return density vs. Normal with VaR line + outlier rug (`item1_viz`)  
**Table:** 4-window VaR summary (use `item1_var`):

| Window | VaR (%) | VaR (cents) |
|--------|---------|-------------|
| Full (2019–) | `r round(item1_var$VaR_Pct[1], 4)`% | `r round(item1_var$VaR_Cents[1], 2)` |
| 60-day | `r round(item1_var$VaR_Pct[2], 4)`% | `r round(item1_var$VaR_Cents[2], 2)` |
| 40-day | `r round(item1_var$VaR_Pct[3], 4)`% | `r round(item1_var$VaR_Cents[3], 2)` |
| 20-day | `r round(item1_var$VaR_Pct[4], 4)`% | `r round(item1_var$VaR_Cents[4], 2)` |

**Talking Points:**
- Historical simulation: VaR = 5th percentile, expressed as positive loss magnitude
- Full-history is most conservative — short windows exclude documented stress events
- **`r nrow(outliers_1)` outlier(s)** outside 0.1%/99.9% bounds: `r paste(format(outliers_1$Date, "%d %b %Y"), collapse = ", ")`
- Empirical distribution is leptokurtic — fat tails justify historical over parametric VaR

---

## Slide 3 — Item 2: Intraday (High–Low) VaR (95%, One-Tail)

**Visual:** Intraday range scatter + LOESS trend + VaR reference line (`item2_viz`)  
**Table:** 4-window intraday VaR summary (use `item2_var`):

| Window | VaR (%) | VaR (cents) |
|--------|---------|-------------|
| Full (2019–) | `r round(item2_var$VaR_Pct[1], 4)`% | `r round(item2_var$VaR_Cents[1], 2)` |
| 60-day | `r round(item2_var$VaR_Pct[2], 4)`% | `r round(item2_var$VaR_Cents[2], 2)` |
| 40-day | `r round(item2_var$VaR_Pct[3], 4)`% | `r round(item2_var$VaR_Cents[3], 2)` |
| 20-day | `r round(item2_var$VaR_Pct[4], 4)`% | `r round(item2_var$VaR_Cents[4], 2)` |

**Talking Points:**
- Range is non-negative → VaR = 95th percentile (upper tail)
- Intraday VaR > close-to-close VaR across **all** windows — prices "whipsaw" intraday before settling
- **`r nrow(outliers_2)` outlier(s)** above 99.9th percentile (`r round(ub_intraday, 2)` cents): `r paste(format(outliers_2$Date, "%d %b %Y"), collapse = ", ")`
- These are the most extreme intraday dislocations — critical for stop-loss and margin exposure

---

## Slide 4 — Item 3: The Volatility Gap (DoD vs. Intraday)

**Visual:** Dual time series — intraday range vs. close-to-close change (`item3_viz`)  
**Table:** VaR gap (use `gap_table`):

| Window | DoD VaR (cts) | Intraday VaR (cts) | Gap (cts) | Gap % of Intraday |
|--------|---------------|---------------------|-----------|-------------------|
| Full | `r round(gap_table$dod_var[1], 2)` | `r round(gap_table$intra_var[1], 2)` | `r round(gap_table$Gap_Cents[1], 2)` | `r round(gap_table$Gap_Pct_of_Intra[1], 1)`% |

**Talking Points:**
- **Market measures risk on a close-to-close basis, BUT intraday ranges dwarf net changes, THEREFORE DoD VaR creates a blind spot**
- The gap is structural: DoD captures only the 4:00 PM BAP fixing delta; it records nothing in between
- Intraday bid-ask swings, BSP interventions, and demand surges that reverse before close are invisible
- **Anyone with intraday obligations, stop-losses, or margin requirements is exposed to this invisible risk**

---

## Slide 5 — Item 4: Solving for Outliers (Coherent Risk Measures)

**Visual:** CVaR vs. VaR threshold density plot (`item4_viz`)  
**Table:** (use `item4_table`):

| Metric | % | Cents |
|--------|---|-------|
| Raw VaR 95% | `r round(item4_table$Percentage[1], 4)`% | `r round(item4_table$Cents[1], 2)` |
| CVaR / Expected Shortfall | `r round(item4_table$Percentage[2], 4)`% | `r round(item4_table$Cents[2], 2)` |
| VaR after Winsorization | `r round(item4_table$Percentage[5], 4)`% | `r round(item4_table$Cents[5], 2)` |
| VaR Reduction (Winsor.) | `r round(item4_table$Percentage[6], 4)` pp | `r round(item4_table$Cents[6], 2)` |

**Talking Points:**
- Historical VaR fails sub-additivity (Artzner et al., 1999) and ignores tail severity
- **CVaR (Expected Shortfall):** mean loss beyond VaR threshold — satisfies all 4 coherence axioms; Basel IV FRTB standard
- **Winsorization:** caps extremes at 0.1%/99.9% bounds — bounds outlier influence without erasing history
- **CVaR is the preferred primary measure**; winsorization serves as a robustness check
- CVaR exceeds raw VaR by `r round(item4_table$Percentage[2] - item4_table$Percentage[1], 4)` pp — quantifies the cost of ignoring tail severity

---

## Slide 6 — Item 5a: Statistical Significance of Time Periods

**Visual:** VaR bar chart across windows (`item5_var_bar`) + distribution overlay (`item5_dist_overlay`)  
**Table:** Significance tests (use `item5_tests`):

| Window | KS Stat | KS p-value | Levene F | Levene p-value |
|--------|---------|------------|----------|----------------|
| 60-day | `r round(item5_tests$KS_Stat[1], 4)` | `r format(item5_tests$KS_p[1], scientific = TRUE)` | `r round(item5_tests$Levene_F[1], 4)` | `r format(item5_tests$Levene_p[1], scientific = TRUE)` |
| 40-day | `r round(item5_tests$KS_Stat[2], 4)` | `r format(item5_tests$KS_p[2], scientific = TRUE)` | `r round(item5_tests$Levene_F[2], 4)` | `r format(item5_tests$Levene_p[2], scientific = TRUE)` |
| 20-day | `r round(item5_tests$KS_Stat[3], 4)` | `r format(item5_tests$KS_p[3], scientific = TRUE)` | `r round(item5_tests$Levene_F[3], 4)` | `r format(item5_tests$Levene_p[3], scientific = TRUE)` |

**Talking Points:**
- **Kolmogorov-Smirnov test:** tests distributional equality vs. full history — all p-values near zero → distributions are fundamentally different
- **Levene test:** tests variance equality — all p-values near zero → volatility structures differ
- Max VaR deviation from full baseline: `r round(max(abs(item5_comp$Diff_from_Full_pp)), 4)` percentage points
- Short windows are **not** drawn from the same statistical population as the full history

---

## Slide 7 — Item 5b: Recency Bias & Window Appropriateness

**Visual:** Rolling 60-day VaR chart (`item5_rolling_var`) — shows pro-cyclical behavior  
**Key Figures:**
- Full history contains **4 regimes**: pre-crisis stability → 2020 COVID shock → 2021–2022 PHP depreciation → 2023–2026 stabilization
- Current 20/40/60-day windows capture **only regime 4**

**Talking Points:**
- **Recency bias:** short windows report safety because conditions are currently calm — they have no memory of stress
- Rolling VaR is pro-cyclical: spikes during crises, collapses during calm — the opposite of a stable risk anchor
- Using short-window VaR as a standalone estimate is **inadequate** for standing risk limits
- **Full-history VaR is the appropriate baseline**; short windows are supplementary indicators of current conditions, not replacements
- The case for full history: it prices in the tail events that will happen again — just not on a predictable schedule

---

## Slide 8 — Item 6a: Portfolio Loss at 99% Confidence

**Visual:** Diverging bar chart — loss vs. upside (`item6_viz`), left panel ("Full Exposure")  
**Key Figures** (use `item6_table`):

| Parameter | Value |
|-----------|-------|
| Reference Date | `r item6_table$Value[1]` |
| FX Rate (PHP/USD) | `r item6_table$Value[2]` |
| VaR 99% | `r item6_table$Value[3]` (`r item6_table$Value[4]` cents) |
| USD Position | `r item6_table$Value[5]` |
| **1-Day Loss @ 99% (USD)** | **`r item6_table$Value[6]`** |
| **1-Day Loss @ 99% (PHP)** | **`r item6_table$Value[7]`** |

**Talking Points:**
- VaR computed at 99% (1st percentile of full DoD history) — more conservative than the 95% used in Items 1–5
- FX rate as of last trading day on or before 30 June 2024: `r item6_table$Value[2]`
- On 1 out of 100 trading days, the actual loss is expected to **exceed** this figure
- This is the unmitigated exposure — the baseline against which the hedge is measured

---

## Slide 9 — Item 6b: Translation Invariance Hedge & Upside Sacrifice

**Visual:** Diverging bar chart (`item6_viz`), right panel ("Capped Loss") + annotation  
**Key Figures** (use `item6_table`):

| Parameter | Value |
|-----------|-------|
| Target Max 1-Day Loss (PHP) | `r item6_table$Value[8]` |
| **Required USD Position** | **`r item6_table$Value[9]`** |
| **USD to Redeploy** | **`r item6_table$Value[10]`** |
| Upside on Full Position (PHP) | `r item6_table$Value[12]` |
| Upside on Reduced Position (PHP) | `r item6_table$Value[13]` |
| **Upside Sacrificed (PHP)** | **`r item6_table$Value[14]`** |

**Talking Points:**
- **Translation invariance** (Artzner et al., 1999): ρ(X − c) = ρ(X) − c — moving cash to the base currency reduces risk by exactly that amount
- Redeploy USD `r item6_table$Value[10]` into **PHP-denominated T-bills** — zero FX exposure, deterministic risk reduction
- FX exposure is symmetric: capping downside at PHP 20,000 simultaneously caps 99th-percentile upside
- **Upside sacrificed: PHP `r item6_table$Value[14]`** — risk reduction and return reduction are the same transaction
- This is not a free lunch; it is an explicit insurance premium

---

## Slide 10 — Synthesis & Recommendations

**No new charts** — summary slide. Use summary table data if space permits.

**Talking Points:**
1. **Close-to-close VaR is incomplete.** Intraday range VaR exceeds DoD VaR by `r round(gap_table$Gap_Pct_of_Intra[1], 1)`% — the "volatility gap" is invisible to standard risk reports
2. **Short windows are inadequate.** KS and Levene tests confirm short windows are statistically distinct from full history (p < 0.001). Recency bias understates tail risk
3. **CVaR replaces VaR.** Expected Shortfall satisfies all coherence axioms, captures tail severity, and exceeds raw VaR by `r round(item4_table$Percentage[2] - item4_table$Percentage[1], 4)` pp
4. **Hedging has a cost.** Capping daily loss at PHP 20,000 requires reducing USD exposure to `r item6_table$Value[9]`, sacrificing `r item6_table$Value[14]` in upside
5. **Recommendation:** Adopt CVaR as the primary risk metric, mandate full-history baselines for risk limits, and explicitly account for intraday volatility in any exposure with intraday obligations

---

## Appendices (Excluded from 10-Slide Count)

Place all detailed tables, outlier listings, and additional figures here:

- **Appendix A:** Full Item 1 VaR table + outlier dates (from `item1_var`, `outliers_1`)
- **Appendix B:** Full Item 2 intraday VaR table + outlier dates (from `item2_var`, `outliers_2`)
- **Appendix C:** Descriptive statistics by window (`item5_desc`)
- **Appendix D:** Winsorization bounds and full comparison table (`item4_table`)
- **Appendix E:** Complete portfolio calculation breakdown (`item6_table`)
- **Appendix F:** Full summary table (from `summary_table` in §10)
