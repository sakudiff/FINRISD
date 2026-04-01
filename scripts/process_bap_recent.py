"""
Recent BAP FX Extraction Engine (2024-2026).
Processes modern Excel summaries featuring standard columnar layouts.
"""

import glob
import os
from typing import List, Dict

import pandas as pd


def process_bap_standard(input_path: str, output_path: str) -> None:
    """
    Extracts and unifies BAP FX data from standard-layout Excel files.
    
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
        
        # Locate the header row by scanning for OHLC markers
        header_row_idx = -1
        for i in range(min(15, len(df))):
            row_vals = [str(val).upper().strip() for val in df.iloc[i].values]
            if "OPEN" in row_vals and "HIGH" in row_vals:
                header_row_idx = i
                break
        
        if header_row_idx == -1:
            print(f"    [WARN] Header row not found in {sheet_name}. Skipping.")
            continue
            
        # Map column indices to features
        headers = [str(val).upper().strip() for val in df.iloc[header_row_idx].values]
        col_map: Dict[int, str] = {}
        for idx, h in enumerate(headers):
            if "OPEN" in h: col_map[idx] = "Open"
            elif "HIGH" in h: col_map[idx] = "High"
            elif "LOW" in h: col_map[idx] = "Low"
            elif "CLOSE" in h: col_map[idx] = "Close"
            elif "DATE" in h or (idx == 0 and h == "NAN"): col_map[idx] = "Date"
        
        data_df = df.iloc[header_row_idx + 1:].copy()
        
        # Build the structured records
        cleaned_rows = []
        for _, row in data_df.iterrows():
            # Mandatory Date parsing
            date_val = row[0] # Assume index 0 is date if mapping fails
            for idx, name in col_map.items():
                if name == "Date":
                    date_val = row[idx]
                    break
            
            dt = pd.to_datetime(date_val, errors='coerce')
            if pd.isna(dt):
                continue
            
            record = {"Date": dt}
            valid_record = True
            for idx, name in col_map.items():
                if name == "Date": continue
                val = pd.to_numeric(row[idx], errors='coerce')
                if pd.isna(val):
                    valid_record = False
                    break
                record[name] = float(val)
            
            if valid_record:
                cleaned_rows.append(record)
        
        if cleaned_rows:
            extracted_series.append(pd.DataFrame(cleaned_rows))
    
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
    """Orchestrates extraction for the 2024-2026 range."""
    years = [2024, 2025, 2026]
    for year in years:
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if matches:
            input_file = matches[0]
            output_file = f"data/unified/unified_{year}_bap.csv"
            process_bap_standard(input_file, output_file)
        else:
            print(f"No file found for year {year} matching {pattern}")


if __name__ == "__main__":
    main()
