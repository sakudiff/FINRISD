"""
BAP FX Gap Analysis Tool.
Identifies missing business days in unified datasets to evaluate data completeness.
"""

import glob
import os
from typing import List, Tuple

import pandas as pd


def analyze_missing_business_days(file_path: str) -> Tuple[int, int, pd.DatetimeIndex]:
    """
    Computes the delta between expected business days and recorded trading days.
    
    Args:
        file_path: Path to the unified CSV file.
        
    Returns:
        A tuple of (Total Business Days, Missing Count, Missing DatetimeIndex).
    """
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    
    # Generate all standard business days (Mon-Fri) as a proxy for trading days.
    # Note: Does not account for Philippine-specific bank holidays.
    all_business_days = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Identify the set difference
    missing_days = all_business_days.difference(df['Date'])
    
    return len(all_business_days), len(missing_days), missing_days


def main() -> None:
    """Orchestrates gap analysis across all extracted yearly datasets."""
    csv_files = sorted(glob.glob("data/unified/unified_20*_bap.csv"))
    
    if not csv_files:
        print("[ERROR] No unified CSVs found. Extraction must precede analysis.")
        return

    print(f"{'Year':<6} | {'Expected (B)':<12} | {'Missing (Days)':<15} | {'Missing %':<10}")
    print("-" * 55)
    
    for file_path in csv_files:
        # Extract year from filename (e.g., unified_2019_bap.csv)
        year = os.path.basename(file_path).split('_')[1]
        total_b, missing_count, missing_list = analyze_missing_business_days(file_path)
        
        pct = (missing_count / total_b) * 100 if total_b > 0 else 0
        print(f"{year:<6} | {total_b:<12} | {missing_count:<15} | {pct:<10.2f}%")
        
        if missing_count > 0:
            samples = ", ".join([d.strftime('%m-%d') for d in missing_list[:10]])
            print(f"  [LOG] Significant gaps detected: {samples}...")


if __name__ == "__main__":
    main()
