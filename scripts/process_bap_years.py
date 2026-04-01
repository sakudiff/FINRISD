"""
Mid-Term BAP FX Extraction Engine (2020-2023).
Processes yearly Excel summaries using a dual-layout detection heuristic.
"""

import glob
import os
from typing import List

import pandas as pd


def process_bap_file(input_path: str, output_path: str) -> None:
    """
    Extracts and unifies BAP FX data from a single yearly Excel file.
    
    Args:
        input_path: Path to the raw Excel file.
        output_path: Destination for the unified CSV.
    """
    if not os.path.exists(input_path):
        print(f"  [ERROR] Source file {input_path} is missing.")
        return

    print(f"Loading {input_path}...")
    xl = pd.ExcelFile(input_path)
    
    extracted_series: List[pd.DataFrame] = []
    
    for sheet_name in xl.sheet_names:
        print(f"  Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Heuristic for layout detection: Check for date concentration in Row 0 vs Column 0.
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            print(f"    [DEBUG] Transposed layout detected.")
            df = df.T
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        else:
            print(f"    [DEBUG] Standard layout detected.")
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
            
        # Standardize column mapping via string matching
        mapping = {}
        for col in df.columns:
            c_str = str(col).upper().strip()
            if 'OPEN' in c_str: mapping[col] = 'Open'
            elif 'HIGH' in c_str: mapping[col] = 'High'
            elif 'LOW' in c_str: mapping[col] = 'Low'
            elif 'CLOSE' in c_str: mapping[col] = 'Close'
            elif 'DATE' in c_str: mapping[col] = 'Date'
        
        df = df.rename(columns=mapping)
        
        # Subset to required OHLC features
        required_cols = ['Date', 'Open', 'High', 'Low', 'Close']
        found_cols = [c for c in required_cols if c in df.columns]
        df = df[found_cols]
        
        # Temporal sanitization
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        # Numerical sanitization
        numeric_cols = ['Open', 'High', 'Low', 'Close']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove empty trading days (metadata artifacts)
        df = df.dropna(subset=numeric_cols, how='all')
        
        extracted_series.append(df)
    
    if not extracted_series:
        print(f"  [WARN] No data extracted from {input_path}.")
        return
        
    unified_df = pd.concat(extracted_series, ignore_index=True)
    unified_df = unified_df.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Invariant Verification: High >= Low
    swapped = (unified_df['High'] < unified_df['Low'])
    if swapped.any():
        print(f"    [FIX] Reconciling {swapped.sum()} rows where High < Low.")
        unified_df.loc[swapped, ['High', 'Low']] = unified_df.loc[swapped, ['Low', 'High']].values
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    unified_df.to_csv(output_path, index=False)
    print(f"Success. Data persisted to {output_path}")


def main() -> None:
    """Orchestrates extraction for the 2020-2023 range."""
    years = [2020, 2021, 2022, 2023]
    for year in years:
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if matches:
            input_file = matches[0]
            output_file = f"data/unified/unified_{year}_bap.csv"
            process_bap_file(input_file, output_file)
        else:
            print(f"No file found for year {year} matching {pattern}")


if __name__ == "__main__":
    main()
