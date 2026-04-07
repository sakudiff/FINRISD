# USD/PHP FX Risk Analysis — 10-Slide Presentation Plan

**Audience:** Prof. Bismark, FINRISD Section C02  
**Constraint:** Maximum 10 slides for submission (appendices excluded from count)  
**Source:** All figures from `fx_analysis.Rmd` → rendered in `index.html`  
**Data:** 1,735 DoD returns (2 Jan 2019 – 27 Feb 2026), cut-off per case guidelines  

---

## Slide 1 — Title & Executive Summary

**Visual:** *"Seven years of USD/PHP"* (`price_history_viz`) — 7-year USD/PHP with shaded stress regimes  
**Key Figures:**
- Data span: 2 Jan 2019 – 27 Feb 2026 (1,735 trading days)
- Full-history DoD VaR 95%: **0.5248% (28.62 cents)**
- Full-history Intraday VaR 95%: **0.7302% (40.00 cents)**

**Talking Points:**
- **What we did:** We conducted a comprehensive forensic audit of USD/PHP exchange rate risk using seven years of BAP data, covering 1,735 trading days from January 2019 through February 2026. This period captures four distinct market regimes — the pre-pandemic stability, the 2020 COVID liquidity shock, the 2021–2022 peso depreciation cycle, and the 2023–2026 stabilization — giving us a full-cycle view of tail risk.
- **The problem we expose:** Standard risk management practice relies on close-to-close Value at Risk computed over short rolling windows — typically the last 20, 40, or 60 trading days. This approach systematically understates risk in two ways. First, it ignores the violent intraday price swings that occur between the open and the 4:00 PM BAP fix. Second, short windows only reflect the current calm regime and erase the memory of past stress events. Our analysis shows that the full-history close-to-close VaR of 0.5248% understates the true intraday risk by 28.45% — a structural blind spot, not a margin of error.
- **Our solution:** We replace standard VaR with Conditional Value at Risk (CVaR), also known as Expected Shortfall, which averages the losses in the entire tail beyond the VaR threshold. CVaR rises to 0.7301% — a 0.2053 percentage-point increase — quantifying the severity of tail events that raw VaR ignores. For the portfolio application, we apply translation invariance, one of the four coherence axioms, to size a hedge that caps daily loss at PHP 20,000.
- **Group members:** Antiado, Bolanos, Patajo, Siapno, Sison, Uy.

---

## Slide 2 — Item 1: Close-to-Close VaR (95%, One-Tail)

**Visual:** *"The long tail of risk"* (`item1_viz`) — return density vs. Normal with VaR line + outlier rug  
**Table:**

| Window | VaR (%) | VaR (cents) |
|--------|---------|-------------|
| Full (2019–) | 0.5248% | 28.62 |
| 60-day | 0.4782% | 28.20 |
| 40-day | 0.4803% | 28.33 |
| 20-day | 0.5005% | 29.48 |

**Talking Points:**
- **Q: What are the four VaR figures using day-on-day closing movement at 95% confidence?**
  **Answer:** Using historical simulation (the empirical 5th percentile, expressed as positive loss magnitude):
  - **(a) Full history from 01 January 2019:** VaR = **0.5248%** or **28.62 PHP cents** per USD — computed from 1,735 trading days.
  - **(b) Past 60 trading days:** VaR = **0.4782%** or **28.20 cents**.
  - **(c) Past 40 trading days:** VaR = **0.4803%** or **28.33 cents**.
  - **(d) Past 20 trading days:** VaR = **0.5005%** or **29.48 cents**.
  The full-history figure is the most conservative. All three short windows understate risk because they exclude the 2020 COVID shock and the 2021–2022 peso depreciation — the exact stress events that produced the largest losses in the dataset.

- **Q: Are there any major outliers? If so, at what dates?**
  **Answer: Yes — four observations fall outside the 0.1st and 99.9th percentile bounds of [−1.5182%, +1.2951%]:**
  - **11 Nov 2022** (−1.65%, −96 cents)
  - **27 Dec 2022** (+1.36%, +75 cents)
  - **06 Feb 2023** (+1.32%, +71 cents)
  - **02 Jan 2025** (−1.83%, −108 cents)
  Each date corresponds to a documented macro stress event. We retained all four in the analysis. Removing outliers to compress the VaR figure would produce a number that understates the full risk spectrum — these are the very events the model exists to anticipate.

- **Q: Why use historical simulation rather than a parametric approach?**
  **Answer:** The density plot ("The long tail of risk") confirms leptokurtosis — the empirical distribution has fatter tails than the Normal reference curve. Large daily moves occur more frequently than a Normal model would predict. A parametric VaR assuming Normality would systematically understate tail risk. Historical simulation lets the data speak for itself.

---

## Slide 3 — Item 2: Intraday (High–Low) VaR (95%, One-Tail)

**Visual:** *"Wide days — intraday volatility over time"* (`item2_viz`) — intraday range scatter + LOESS trend + VaR reference line  
**Table:**

| Window | VaR (%) | VaR (cents) |
|--------|---------|-------------|
| Full (2019–) | 0.7302% | 40.00 |
| 60-day | 0.4991% | 29.40 |
| 40-day | 0.4991% | 29.40 |
| 20-day | 0.6528% | 37.50 |

**Talking Points:**
- **Q: What are the four VaR figures using daily high-to-low movement at 95% confidence?**
  **Answer:** Since the daily range (High − Low) is always non-negative, the VaR is the 95th percentile of the upper tail:
  - **(a) Full history from 01 January 2019:** VaR = **0.7302%** or **40.00 PHP cents**.
  - **(b) Past 60 trading days:** VaR = **0.4991%** or **29.40 cents**.
  - **(c) Past 40 trading days:** VaR = **0.4991%** or **29.40 cents**.
  - **(d) Past 20 trading days:** VaR = **0.6528%** or **37.50 cents**.
  The full-history intraday VaR of 40.00 cents is nearly double the short-window figures, confirming that the most extreme intraday dislocations occurred during the 2020–2022 stress period and are absent from recent windows.

- **Q: Are there any major outliers? If so, at what dates?**
  **Answer: Yes — two trading days exceed the 99.9th percentile intraday range threshold of 100.63 cents (over PHP 1.00):**
  - **04 Sep 2019:** Range = 101 cents (1.95%). High = 52.93, Low = 51.92.
  - **12 Sep 2024:** Range = 112 cents (2.03%). High = 56.20, Low = 55.08.
  These are the most extreme intraday dislocations in the full dataset — sessions where the peso swung by over a full peso within a single trading day. Any market participant with intraday stop-loss orders, margin calls, or hedging triggers would have been exposed to the full range of these moves, regardless of where the price ultimately closed.

- **Q: How does this differ methodologically from Item 1?**
  **Answer:** Item 1 measures the net change from one day's close to the next (the 5th percentile of a distribution that includes both gains and losses). Item 2 measures the total distance traveled within a single day (the 95th percentile of a distribution that is always positive). Item 1 answers: "How much can I lose from yesterday's close?" Item 2 answers: "How far can the price move against me within a single day?" The answer to the second question is consistently worse.

---

## Slide 4 — Item 3: The Volatility Gap (DoD vs. Intraday)

**Visual:** *"Mind the gap"* (`item3_viz`) — dual time series: intraday range vs. close-to-close change  
**Table:**

| Window | DoD VaR (cts) | Intraday VaR (cts) | Gap (cts) | Gap % of Intra |
|--------|---------------|---------------------|-----------|----------------|
| Full | 28.62 | 40.00 | 11.38 | 28.45% |
| 60-day | 28.20 | 29.40 | 1.20 | 4.08% |
| 40-day | 28.33 | 29.40 | 1.08 | 3.66% |
| 20-day | 29.48 | 37.50 | 8.02 | 21.39% |

**Talking Points:**
- **Q: Will using only closing-to-closing movements in USD/PHP potentially miss out any potential volatility? Explain.**
  **Answer: Yes, it will — and the magnitude of what is missed is substantial, not marginal.** The full-history intraday VaR of 40.00 cents exceeds the close-to-close VaR of 28.62 cents by **11.38 cents, or 28.45% of the intraday figure**. Nearly one-third of the risk embedded in USD/PHP is invisible to any model that only examines closing prices. This pattern holds across every window: the 60-day gap is 1.20 cents (4.08%), the 40-day gap is 1.08 cents (3.66%), and the 20-day gap is 8.02 cents (21.39%). The gap is structural, not incidental.

- **Q: Why does this gap exist?**
  **Answer:** The close-to-close change captures only the net price movement between one day's 4:00 PM BAP fixing and the next. It records nothing of what occurs in between. During the trading day, USD/PHP is subject to intraday bid-ask spread widening, BSP intervention responses, corporate dollar demand surges, and algorithmic trading flows — all of which can push the price far from the open before the close. Consider a session where the pair opens at PHP 57.00, spikes to PHP 57.90 on a dollar-demand surge, then retreats to close at PHP 57.10. The DoD change registers only PHP 0.10. The intraday range was PHP 0.90. A risk manager using DoD VaR classifies that session as low-risk. Anyone with a stop-loss at PHP 57.50 would have been stopped out.

- **Q: Who is exposed to this invisible risk?**
  **Answer:** Any market participant with intraday obligations — corporate treasurers executing hedging orders at specific intraday levels, traders managing stop-loss triggers, institutions with margin requirements that must be met intraday, and portfolio managers rebalancing positions before the close. The *"Mind the gap"* chart confirms that the intraday range (blue) consistently exceeds the signed close-to-close change (red) across the full 2019–2026 history, and the divergence widens dramatically during the 2020 COVID shock and the 2022 depreciation episode. The gap expands precisely when risk management matters most.

---

## Slide 5 — Item 4: Solving for Outliers (Coherent Risk Measures)

**Visual:** *"Beyond the threshold: Expected Shortfall"* (`item4_viz`) — CVaR vs. VaR threshold density plot  
**Table:**

| Metric | % | Cents |
|--------|---|-------|
| Raw VaR 95% | 0.5248% | 28.62 |
| CVaR / Expected Shortfall | 0.7301% | 40.68 |
| VaR after Winsorization | 0.5248% | 28.62 |
| VaR Reduction (Winsor.) | 0.0000 pp | 0.00 |

**Talking Points:**
- **Q: How can you possibly solve for the problem of outliers? Explain and illustrate.**
  **Answer: We present two solutions, both grounded in the coherent risk measure framework of Artzner et al. (1999):**

  **Solution 1 — CVaR (Expected Shortfall):** CVaR replaces VaR as the primary risk measure. VaR tells you the threshold of loss ("you will lose at least X with 5% probability") but says nothing about what happens beyond that threshold. CVaR answers the follow-up question: "Given that we've breached the 5th percentile, how bad is the average loss?" For our full history, CVaR = **0.7301% (40.68 cents)** — significantly higher than raw VaR of 0.5248% (28.62 cents). The difference of **0.2053 percentage points** quantifies the severity of tail losses that VaR ignores. CVaR satisfies all four coherence axioms (monotonicity, sub-additivity, positive homogeneity, translation invariance) and is the regulatory standard under Basel IV's Fundamental Review of the Trading Book. By averaging across the entire tail, CVaR automatically incorporates outlier severity — the extreme observations at 04 Sep 2019, 11 Nov 2022, 02 Jan 2025, and others pull the CVaR upward in direct proportion to their magnitude. This is the correct behavior: outliers should increase the risk measure, not be discarded.

  **Solution 2 — Winsorization:** As a robustness check, we capped extreme returns at the 0.1st and 99.9th percentile bounds (−1.5182% and +1.2951%) rather than removing them. This bounds the influence of outliers without erasing them from the dataset. The result: VaR after winsorization = **0.5248%** — identical to raw VaR, with **zero reduction**. This confirms that the 5th-percentile VaR threshold sits well inside the winsorization bounds, so the extreme outliers at the 0.1% level are too far out to affect the 5th percentile. Winsorization is useful as a diagnostic tool but does not resolve VaR's sub-additivity failure.

- **Q: Which solution is preferred?**
  **Answer:** CVaR is the preferred primary measure. It captures tail severity, satisfies all coherence axioms, and is regulatorily endorsed. Winsorization serves as a supplementary robustness check — in this case confirming that the VaR figure is not being driven by a single extreme observation.

---

## Slide 6 — Item 5a: Statistical Significance of Time Periods

**Visuals:** *"Stability in numbers"* (`item5_var_bar`) — VaR bar chart across windows; *"Same currency, different stories"* (`item5_dist_overlay`) — distribution overlay  
**Table:**

| Window | KS Stat | KS p-value | Levene F | Levene p-value |
|--------|---------|------------|----------|----------------|
| 60-day | 0.0971 | 0.6453 | 0.7324 | 0.4640 |
| 40-day | 0.1099 | 0.7327 | 0.5694 | 0.5691 |
| 20-day | 0.2066 | 0.3673 | 0.0647 | 0.9484 |

**Talking Points:**
- **Q: Are the differences between VaR for various time periods significant? (20, 40, 60 days vs. historical from 2019?)**
  **Answer: The differences are economically significant but statistically non-significant — and the statistical non-significance is a false negative.** We ran two formal tests:
  - **Kolmogorov-Smirnov test** (tests whether two samples come from the same cumulative distribution):
    - w60 vs. Full: KS = 0.0971, **p = 0.6453**
    - w40 vs. Full: KS = 0.1099, **p = 0.7327**
    - w20 vs. Full: KS = 0.2066, **p = 0.3673**
  - **Levene test** (tests whether two samples have equal variances):
    - w60 vs. Full: F = 0.7324, **p = 0.4640**
    - w40 vs. Full: F = 0.5694, **p = 0.5691**
    - w20 vs. Full: F = 0.0647, **p = 0.9484**
  All p-values are high — we fail to reject the null hypothesis in every case. Statistically, the short windows appear indistinguishable from the full history. But this is misleading. The KS test evaluates the entire cumulative distribution, not just the tails, and is notoriously underpowered for detecting tail-specific differences in small samples of 20–60 observations. The Levene test evaluates overall variance equality, but the critical difference lies in tail behavior, not overall dispersion. The max VaR deviation from the full-history baseline is **0.0466 percentage points** (the 60-day window). While the tests cannot detect this as statistically significant, a VaR figure that understates tail risk by nearly 9% is a structural underestimation with real consequences for capital adequacy and hedging decisions.

---

## Slide 7 — Item 5b: Recency Bias & Window Appropriateness

**Visual:** *"VaR is not static"* (`item5_rolling_var`) — rolling 60-day VaR chart showing pro-cyclical behavior  
**Key Figures:**
- Full history contains **4 regimes**: pre-crisis stability → 2020 COVID shock → 2021–2022 PHP depreciation → 2023–2026 stabilization
- Current 20/40/60-day windows capture **only regime 4**
- Descriptive stats: Full SD = 0.3361; w60 SD = 0.2878; w40 SD = 0.2894; w20 SD = 0.3148 — short windows show compressed volatility and negative skew

**Talking Points:**
- **Q: Is it appropriate to use only the data from past 20/40/60 days VaR rather than all the way from 2019?**
  **Answer: No, it is not appropriate.** Using only short-window VaR as a standalone estimate is inadequate for standing risk limits. Here is why:

  **The full 2019–2026 history contains four structurally distinct market regimes:**
  1. **Pre-crisis stability (2019 – early 2020):** USD/PHP traded in a narrow band with low volatility.
  2. **2020 COVID shock:** Global liquidity dried up and USD/PHP experienced its most extreme daily swings — the environment that produced the largest single-day losses in the dataset.
  3. **2021–2022 peso depreciation:** Aggressive Fed rate hikes and elevated commodity import costs pushed the peso past PHP 59/USD in a sustained downtrend.
  4. **2023–2026 stabilization:** The Fed paused and BSP interventions restored relative calm.

  The 20-day, 40-day, and 60-day windows capture **only regime 4** — the current calm. They have no memory of the 2020 shock or the 2022 depreciation. This is recency bias: the model reports safety because conditions are currently safe. The descriptive statistics confirm this — short windows show compressed standard deviations (0.2878–0.3148 vs. 0.3361 for the full history) and negative skew (−0.43 to −0.91), indicating recent returns have been drifting lower with reduced dispersion.

  **The rolling VaR chart ("VaR is not static") is the most diagnostic visual:** The 60-day rolling VaR behaves pro-cyclically. It spiked above 1.0% during the 2020 COVID shock, rose again during the 2022 depreciation, and has since collapsed to its current level below 0.50%. It expands during crises — when you already know you're in trouble — and contracts during calm periods — precisely when a robust risk measure should be warning you that the next shock is coming. This is the opposite of what a risk anchor should do.

  **Our conclusion:** The full-history VaR is the appropriate baseline for standing risk limits because it prices in the full spectrum of tail events — the ones that have happened and the ones that will happen again. Short-window figures (20/40/60 days) are useful as supplementary indicators of current market conditions, but they are not replacements for the full-cycle risk baseline.

---

## Slide 8 — Item 6a: Portfolio Loss at 99% Confidence

**Visual:** *"The price of safety"* (`item6_viz`), left panel — "Full Exposure (USD 10M)"  
**Key Figures:**

| Parameter | Value |
|-----------|-------|
| Reference Date | 28 Jun 2024 |
| FX Rate (PHP/USD) | 58.61 |
| VaR 99% | 0.7974% (44.76 cents) |
| USD Position | 10,000,000 |
| **1-Day Loss @ 99% (USD)** | **79,739.69** |
| **1-Day Loss @ 99% (PHP)** | **4,673,543** |

**Talking Points:**
- **Q: If a portfolio as of 30 June 2024 includes USD cash of 10,000,000.00, at the 99% level of confidence, how much can it possibly lose from a single day?**
  **Answer:** We compute the 99% VaR — the 1st percentile of the full DoD return distribution — which is **0.7974%**, equivalent to **44.76 PHP cents** per USD. This is a more conservative threshold than the 95% VaR of 0.5248% used in Items 1–5. The jump from 95% to 99% represents a **52% increase** in the risk figure (0.5248% → 0.7974%), reflecting the fat-tailed nature of the distribution. The FX rate used is the BAP closing rate on the last trading day on or before 30 June 2024: **28 June 2024 at PHP 58.61 per USD**.

  The calculation:
  - **USD loss:** 0.7974% × USD 10,000,000 = **USD 79,739.69**
  - **PHP loss:** USD 79,739.69 × 58.61 = **PHP 4,673,543**

  On 99 out of 100 trading days, the single-day loss will not exceed this figure. But on the remaining 1 day in 100 — roughly once every five months — the actual loss will be worse. For a portfolio of this size, PHP 4.67 million is not an abstract number; it is a material hit to the firm's financial position.

---

## Slide 9 — Item 6b: Translation Invariance Hedge & Upside Sacrifice

**Visual:** *"The price of safety"* (`item6_viz`), right panel — "Capped Loss (PHP 20K target)"  
**Key Figures:**

| Parameter | Value |
|-----------|-------|
| Target Max 1-Day Loss (PHP) | 20,000 |
| **Required USD Position** | **42,794.08** |
| **USD to Redeploy** | **9,957,206** |
| 99th Percentile Upside (%) | 0.9155% |
| Upside on Full Position (PHP) | 5,365,528 |
| Upside on Reduced Position (PHP) | 22,961.29 |
| **Upside Sacrificed (PHP)** | **5,342,567** |

**Talking Points:**
- **Q: If we want to reduce the potential loss to PHP 20,000, would it be appropriate to reduce the amount of USD holdings? If so, what asset class should we move the amount to?**
  **Answer: Yes, it is appropriate — and the mechanism is translation invariance**, one of the four coherence axioms established by Artzner et al. (1999). Translation invariance states that adding a risk-free cash amount *c* in the base currency reduces the portfolio's risk measure by exactly *c*. Formally, ρ(X − c) = ρ(X) − c. In practical terms: if we move PHP-denominated assets into the portfolio, the FX risk declines by exactly that PHP amount.

  To cap the daily loss at PHP 20,000, we solve for the USD position where the 99% VaR equals PHP 20,000:
  - **Required USD position:** **USD 42,794.08**
  - **USD to redeploy:** **USD 9,957,206** (99.57% of the original position)

  The appropriate asset class for the redeployed funds is **PHP-denominated cash or Philippine government Treasury bills**. These instruments carry zero FX exposure relative to the PHP base currency, eliminating all currency risk on the redeployed amount. This is the correct application of translation invariance: we are adding a risk-free asset in the base currency to mechanically reduce the portfolio's FX risk by a deterministic amount.

- **Q: Will the reduction in USD holdings also potentially reduce the possible upside?**
  **Answer: Yes — because FX exposure is symmetric.** The same position that generates downside risk when the peso strengthens generates upside gain when the peso weakens. The 99th-percentile upside of the full USD 10M position is 0.9155%, equivalent to **PHP 5,365,528**. After reducing the position to USD 42,794, the upside falls to **PHP 22,961.29**. The upside sacrificed is **PHP 5,342,567** — nearly the mirror image of the downside avoided. Risk reduction and return reduction are the same transaction. There is no free lunch.

  The *"The price of safety"* chart makes this trade-off visually explicit. The full-exposure panel shows bars of PHP 4.67M (loss) and PHP 5.37M (upside). The capped-loss panel shows bars of PHP 20K (loss) and PHP 23K (upside). The risk manager must decide whether the certainty of a PHP 20,000 maximum loss is worth giving up PHP 5.34 million in potential gain. This is not a mathematical question — it is a strategic one.

---

## Slide 10 — Synthesis & Recommendations

**No new charts** — summary slide.

**Talking Points:**
1. **Items 1 & 2 — Four VaR figures each, with outliers identified.** The close-to-close VaR (Item 1) at 95% confidence ranges from 0.4782% (60-day) to 0.5248% (full history), presented in both cents and percentage. Four outliers were identified outside the 99.9% bounds: 11 Nov 2022, 27 Dec 2022, 06 Feb 2023, and 02 Jan 2025. The intraday VaR (Item 2) ranges from 0.4991% (60-day/40-day) to 0.7302% (full history). Two outliers exceed the 99.9th percentile: 04 Sep 2019 and 12 Sep 2024. In every window, intraday VaR exceeds close-to-close VaR.

2. **Item 3 — Yes, close-to-close misses volatility.** The intraday range VaR exceeds the close-to-close VaR by 11.38 cents (28.45% of the intraday figure) on the full history. The gap is structural and widens during stress periods. Anyone with intraday obligations — stop-losses, margin calls, hedging triggers — is exposed to risk that DoD VaR does not capture.

3. **Item 4 — Two solutions for outlier sensitivity.** CVaR (Expected Shortfall) = 0.7301% (40.68 cents), exceeding raw VaR by 0.2053 pp. CVaR satisfies all four coherence axioms and is the Basel IV FRTB standard. Winsorization at the 0.1%/99.9% bounds produced zero reduction, confirming that VaR is not being driven by single extreme observations, but winsorization does not fix VaR's sub-additivity failure. CVaR is the preferred primary measure.

4. **Item 5 — Differences are economically significant but statistically non-significant.** KS and Levene tests fail to reject equality (all p > 0.36), but this is a false negative from underpowered tests on small samples. Short windows are **not appropriate** as standalone risk baselines because they capture only the current calm regime and exclude the 2020 COVID shock and 2022 peso depreciation. The full-history VaR is the appropriate baseline.

5. **Item 6 — Portfolio loss, hedge sizing, and upside trade-off.** A USD 10M position faces a 99% single-day loss of PHP 4,673,543. Capping the loss at PHP 20,000 requires reducing the position to USD 42,794 via translation invariance, redeploying USD 9,957,206 into PHP T-bills. This sacrifices PHP 5,342,567 in upside — risk reduction and return reduction are the same transaction.

---

## Appendices (Excluded from 10-Slide Count)

Place all detailed tables, outlier listings, and additional figures here:

### Appendix A — Item 1: Close-to-Close VaR (95%, One-Tail)

**Figure A1:** *"The long tail of risk"* (`item1_viz`) — return density vs. Normal with VaR line + outlier rug  
**Figure A2:** *"Seven years of USD/PHP"* (`price_history_viz`) — full price history with shaded analysis windows  

**Table A1: VaR by Window**

| Window | n | VaR (%) | VaR (cents) |
|--------|---|---------|-------------|
| Full (2019–) | 1,735 | 0.5248 | 28.62 |
| 60-day | 60 | 0.4782 | 28.20 |
| 40-day | 40 | 0.4803 | 28.33 |
| 20-day | 20 | 0.5005 | 29.48 |

**Table A2: Outliers — DoD % outside [−1.5182%, +1.2951%] (0.1%/99.9% bounds)**

| Date | Close | DoD (%) | DoD (cents) |
|------|-------|---------|-------------|
| 11 Nov 2022 | 57.23 | −1.6498 | −96 |
| 27 Dec 2022 | 55.90 | +1.3599 | +75 |
| 06 Feb 2023 | 54.39 | +1.3227 | +71 |
| 02 Jan 2025 | 57.91 | −1.8308 | −108 |

---

### Appendix B — Item 2: Intraday (High–Low) VaR (95%, One-Tail)

**Figure B1:** *"Wide days — intraday volatility over time"* (`item2_viz`) — intraday range scatter + LOESS trend + VaR reference line  

**Table B1: VaR by Window**

| Window | n | VaR (cents) | VaR (%) |
|--------|---|-------------|---------|
| Full (2019–) | 1,736 | 40.00 | 0.7302 |
| 60-day | 60 | 29.40 | 0.4991 |
| 40-day | 40 | 29.40 | 0.4991 |
| 20-day | 20 | 37.50 | 0.6528 |

**Table B2: Outliers — Intraday range above 100.63 cents (99.9th percentile)**

| Date | High | Low | Intraday (cents) | Intraday (%) |
|------|------|-----|-------------------|--------------|
| 04 Sep 2019 | 52.93 | 51.92 | 101 | 1.9453 |
| 12 Sep 2024 | 56.20 | 55.08 | 112 | 2.0334 |

---

### Appendix C — Item 3: VaR Gap (Intraday − DoD)

**Figure C1:** *"Mind the gap"* (`item3_viz`) — dual time series: intraday range vs. close-to-close change  

**Table C1: Gap by Window**

| Window | DoD VaR (cents) | Intraday VaR (cents) | Gap (cents) | Gap % of Intra |
|--------|-----------------|-----------------------|-------------|----------------|
| Full | 28.62 | 40.00 | 11.38 | 28.45% |
| 60-day | 28.20 | 29.40 | 1.20 | 4.08% |
| 40-day | 28.33 | 29.40 | 1.08 | 3.66% |
| 20-day | 29.48 | 37.50 | 8.02 | 21.39% |

---

### Appendix D — Item 4: CVaR & Winsorization (Full History)

**Figure D1:** *"Beyond the threshold: Expected Shortfall"* (`item4_viz`) — CVaR vs. VaR threshold density plot  

**Table D1: Coherent Risk Measures**

| Metric | % | Cents |
|--------|---|-------|
| Raw VaR (95%) | 0.5248 | 28.62 |
| CVaR / Expected Shortfall (95%) | 0.7301 | 40.68 |
| Winsorization Lower Bound (0.1%) | −1.5182 | — |
| Winsorization Upper Bound (99.9%) | +1.2951 | — |
| VaR after Winsorization (95%) | 0.5248 | 28.62 |
| VaR Reduction from Winsorization | 0.0000 pp | 0.00 |

---

### Appendix E — Item 5: Statistical Significance

**Figure E1:** *"Stability in numbers"* (`item5_var_bar`) — VaR bar chart across windows  
**Figure E2:** *"Same currency, different stories"* (`item5_dist_overlay`) — overlaid return density curves  
**Figure E3:** *"VaR is not static"* (`item5_rolling_var`) — rolling 60-day VaR chart showing pro-cyclical behavior  

**Table E1: KS & Levene Tests (each window vs. full history)**

| Window | n | KS Stat | KS p-value | Levene F | Levene p-value |
|--------|---|---------|------------|----------|----------------|
| 60-day | 60 | 0.0971 | 0.6453 | 0.7324 | 0.4640 |
| 40-day | 40 | 0.1099 | 0.7327 | 0.5694 | 0.5691 |
| 20-day | 20 | 0.2066 | 0.3673 | 0.0647 | 0.9484 |

**Table E2: Descriptive Statistics by Window**

| Window | n | Mean | SD | Skew | Kurtosis |
|--------|---|------|----|------|----------|
| Full | 1,735 | 0.0060 | 0.3361 | 0.0457 | 2.1106 |
| 60-day | 60 | −0.0332 | 0.2878 | −0.4345 | 0.9081 |
| 40-day | 40 | −0.0479 | 0.2894 | −0.8464 | 0.9938 |
| 20-day | 20 | −0.1092 | 0.3148 | −0.9053 | 0.6524 |

**Table E3: VaR Comparison — Difference from Full-History Baseline**

| Window | n | VaR (%) | VaR (cents) | Diff from Full (pp) |
|--------|---|---------|-------------|---------------------|
| Full | 1,735 | 0.5248 | 28.62 | 0.0000 |
| 60-day | 60 | 0.4782 | 28.20 | −0.0466 |
| 40-day | 40 | 0.4803 | 28.33 | −0.0445 |
| 20-day | 20 | 0.5005 | 29.48 | −0.0243 |

---

### Appendix F — Item 6: Portfolio Loss & Hedge Sizing (99% Confidence)

**Figure F1:** *"The price of safety"* (`item6_viz`) — diverging bar chart: loss vs. upside, two panels (full exposure vs. capped loss)  

**Table F1: Complete Calculation**

| Parameter | Value |
|-----------|-------|
| Reference Date | 28 Jun 2024 |
| FX Rate (PHP/USD) | 58.61 |
| Full-History VaR 99% (%) | 0.7974 |
| VaR 99% (cents) | 44.764 |
| USD Position | 10,000,000 |
| 1-Day Loss @ 99% (USD) | 79,739.69 |
| 1-Day Loss @ 99% (PHP) | 4,673,543 |
| Target Max 1-Day Loss (PHP) | 20,000 |
| Required USD Position | 42,794.08 |
| USD to Redeploy | 9,957,206 |
| 99th Percentile Upside (%) | 0.9155 |
| Upside on Full Position (PHP) | 5,365,528 |
| Upside on Reduced Position (PHP) | 22,961.29 |
| Upside Sacrificed (PHP) | 5,342,567 |
