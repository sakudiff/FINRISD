
# Deep Cross-Validation for USD/PHP FX Risk Analysis
# No libraries (except readr for speed) to ensure raw logic is visible

df <- read.csv("data/consolidated_usdphp.csv")
df$Date <- as.Date(df$Date)
df <- df[order(df$Date), ]

# 1. Manual Error Fix
error_rows <- which(df$High < df$Low)
for(i in error_rows) {
    tmp <- df$High[i]
    df$High[i] <- df$Low[i]
    df$Low[i] <- tmp
}

# 2. Raw Return Calculation
n <- nrow(df)
dod_pct <- (df$Close[2:n] - df$Close[1:(n-1)]) / df$Close[1:(n-1)] * 100
dod_cents <- (df$Close[2:n] - df$Close[1:(n-1)]) * 100
intraday_pct <- (df$High - df$Low) / df$Low * 100
intraday_cents <- (df$High - df$Low) * 100

# 3. Item 1: DoD VaR 95% (Full)
# type=7 is the R default and the Excel/MATLAB standard
var_pct_95 <- quantile(dod_pct, 0.05, type = 7)
var_cents_95 <- quantile(dod_cents, 0.05, type = 7)

# 4. Outlier Validation (DoD 99.9% bounds)
lb_999 <- quantile(dod_pct, 0.001, type = 7)
ub_999 <- quantile(dod_pct, 0.999, type = 7)
outlier_indices <- which(dod_pct < lb_999 | dod_pct > ub_999)
outlier_dates <- df$Date[outlier_indices + 1] # +1 because dod_pct starts at index 2

# 5. Item 2: Intraday VaR 95% (Full)
var_intra_cents_95 <- quantile(intraday_cents, 0.95, type = 7)

# 6. Item 6: Portfolio (Manual Check)
# Find June 28, 2024 (nearest trading day to June 30)
ref_idx <- max(which(df$Date <= as.Date("2024-06-30")))
ref_date <- df$Date[ref_idx]
ref_px <- df$Close[ref_idx]

var_99_pct <- quantile(dod_pct, 0.01, type = 7)
loss_php_10m <- abs(var_99_pct / 100) * 10000000 * ref_px

# Target PHP 20,000 loss
target_pos_usd <- 20000 / (abs(var_99_pct / 100) * ref_px)

# Output for Agent Review
cat("--- DEEP VERIFICATION RESULTS ---\n")
cat("Total Rows:", nrow(df), "\n")
cat("DoD Return Rows:", length(dod_pct), "\n")
cat("VaR 95% DoD (%):", var_pct_95, "\n")
cat("VaR 95% DoD (cents):", var_cents_95, "\n")
cat("Outlier Lower Bound (0.1%):", lb_999, "\n")
cat("Outlier Upper Bound (99.9%):", ub_999, "\n")
cat("Outlier Dates Identified:", as.character(outlier_dates), "\n")
cat("VaR 95% Intraday (cents):", var_intra_cents_95, "\n")
cat("Reference Date Used:", as.character(ref_date), " (Price:", ref_px, ")\n")
cat("Portfolio 1-Day Loss (PHP):", loss_php_10m, "\n")
cat("Target USD Position for 20k Loss:", target_pos_usd, "\n")
cat("--- END VERIFICATION ---\n")
