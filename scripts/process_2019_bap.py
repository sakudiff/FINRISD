"""
2019 BAP FX Extraction Engine.
Extracts OHLC data from the 2019 Excel summary, which features a mix of 
transposed and standard layouts.
"""

import os
from typing import List, Optional

import pandas as pd


def process_2019_bap(input_path: str, output_path: str) -> None:
    """
    Extracts and unifies 2019 BAP FX data from Excel sheets.
    
    Args:
        input_path: Path to the raw 2019 Excel file.
        output_path: Destination for the unified CSV.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file {input_path} is missing. Impossible to proceed.")

    print(f"Loading {input_path}...")
    xl = pd.ExcelFile(input_path)
    
    extracted_series: List[pd.DataFrame] = []
    
    for sheet_name in xl.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Heuristic for layout detection: Check for date concentration in Row 0 vs Column 0.
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            print(f"  [DEBUG] Transposed layout detected for {sheet_name}.")
            df = df.T
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        else:
            print(f"  [DEBUG] Standard layout detected for {sheet_name}.")
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
        print("Warning: No data extracted from any sheet.")
        return
        
    unified_df = pd.concat(extracted_series, ignore_index=True)
    unified_df = unified_df.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Invariant Verification: High >= Low
    swapped = (unified_df['High'] < unified_df['Low'])
    if swapped.any():
        print(f"  [FIX] Reconciling {swapped.sum()} rows where High < Low.")
        unified_df.loc[swapped, ['High', 'Low']] = unified_df.loc[swapped, ['Low', 'High']].values
    
    unified_df.to_csv(output_path, index=False)
    print(f"Success. Unified 2019 data persisted to {output_path}")


if __name__ == "__main__":
    process_2019_bap(
        input_path="data/2019 BAP FX Summary.xlsx",
        output_path="data/unified/unified_2019_bap.csv"
    )
