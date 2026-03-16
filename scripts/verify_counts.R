library(readr)
library(dplyr)
library(lubridate)

df_all <- read_csv("data/unified_usdphp_bap.csv", show_col_types = FALSE)
df_trading <- df_all %>% filter(wday(Date) %in% 2:6)
df_returns <- df_trading %>% 
  mutate(dod_pct = (Close - lag(Close)) / lag(Close)) %>% 
  filter(!is.na(dod_pct))

cat("Total days:", nrow(df_all), "\n")
cat("Trading days:", nrow(df_trading), "\n")
cat("Return observations:", nrow(df_returns), "\n")
cat("Start date:", as.character(min(df_trading$Date)), "\n")
cat("End date:", as.character(max(df_trading$Date)), "\n")
