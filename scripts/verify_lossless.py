"""
BAP FX Lossless Verification Tool.
Audits the extraction process by comparing raw Excel row counts and values 
against the unified CSV outputs.
"""

import glob
import os
from typing import List, Tuple, Optional

import pandas as pd


def count_excel_records(file_path: str) -> Tuple[int, List[Tuple[pd.Timestamp, float]]]:
    """
    Heuristically counts valid trading records in an Excel file.
    
    Args:
        file_path: Path to the raw Excel file.
        
    Returns:
        A tuple of (Total Record Count, List of (Date, Close) samples for spot-checking).
    """
    xl = pd.ExcelFile(file_path)
    total_records = 0
    samples: List[Tuple[pd.Timestamp, float]] = []
    
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Determine layout (Transposed vs Standard)
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            # Row-based features
            close_row_idx = -1
            for i in range(len(df)):
                label = str(df.iloc[i, 0]).upper().strip()
                if label == "CLOSE":
                    close_row_idx = i
                    break
            
            if close_row_idx != -1:
                closes = pd.to_numeric(df.iloc[close_row_idx, 1:], errors='coerce')
                dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
                valid_mask = closes.notna() & dates.notna()
                total_records += int(valid_mask.sum())
                
                if valid_mask.any():
                    idx = valid_mask.idxmax()
                    samples.append((pd.Timestamp(dates[idx]), float(closes[idx])))
        else:
            # Column-based features
            header_row_idx = -1
            for i in range(min(15, len(df))):
                row_vals = [str(val).upper().strip() for val in df.iloc[i].values]
                if "OPEN" in row_vals and "CLOSE" in row_vals:
                    header_row_idx = i
                    break
            
            if header_row_idx != -1:
                headers = [str(val).upper().strip() for val in df.iloc[header_row_idx].values]
                close_col_idx = headers.index("CLOSE")
                
                closes = pd.to_numeric(df.iloc[header_row_idx+1:, close_col_idx], errors='coerce')
                dates = pd.to_datetime(df.iloc[header_row_idx+1:, 0], errors='coerce')
                valid_mask = closes.notna() & dates.notna()
                total_records += int(valid_mask.sum())
                
                if valid_mask.any():
                    idx = valid_mask.idxmax()
                    samples.append((pd.Timestamp(dates[idx]), float(closes[idx])))
                    
    return total_records, samples


def main() -> None:
    """Orchestrates the lossless verification audit."""
    years = range(2019, 2027)
    
    print(f"{'Year':<6} | {'Excel Recs':<12} | {'CSV Recs':<10} | {'Status':<12}")
    print("-" * 55)
    
    for year in years:
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if not matches:
            continue
            
        excel_path = matches[0]
        csv_path = f"data/unified/unified_{year}_bap.csv"
        
        if not os.path.exists(csv_path):
            print(f"{year:<6} | {'MISSING':<12} | {'-':<10} | {'-':<12}")
            continue
            
        # Audit Excel
        excel_count, samples = count_excel_records(excel_path)
        
        # Audit CSV
        csv_df = pd.read_csv(csv_path)
        csv_count = len(csv_df)
        csv_df['Date'] = pd.to_datetime(csv_df['Date'])
        
        status = "VERIFIED" if excel_count == csv_count else f"DELTA({csv_count - excel_count:+})"
        
        # Perform Spot Check on specific values
        for s_date, s_close in samples:
            match_row = csv_df[csv_df['Date'] == s_date]
            if match_row.empty:
                status = "MISSING DATE"
                break
            if abs(match_row.iloc[0]['Close'] - s_close) > 1e-5:
                status = "VAL MISMATCH"
                break
            
        print(f"{year:<6} | {excel_count:<12} | {csv_count:<10} | {status:<12}")
        
    print("-" * 55)
    print("Audit process concluded.")


if __name__ == "__main__":
    main()
