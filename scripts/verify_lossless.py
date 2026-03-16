import pandas as pd
import glob
import os

def count_excel_rows(file_path):
    xl = pd.ExcelFile(file_path)
    total_valid_rows = 0
    sample_values = []
    
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Detection logic for 2019-2023 (transposed vs standard)
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            # Dates in Row 0, Data in Rows below (OPEN, HIGH, LOW, CLOSE)
            # Find which row has "CLOSE"
            close_row_idx = -1
            for i in range(len(df)):
                if str(df.iloc[i, 0]).upper().strip() == "CLOSE":
                    close_row_idx = i
                    break
            
            if close_row_idx != -1:
                # Count valid numeric closes in that row
                closes = pd.to_numeric(df.iloc[close_row_idx, 1:], errors='coerce')
                dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
                valid_mask = closes.notna() & dates.notna()
                total_valid_rows += valid_mask.sum()
                
                # Pick a sample
                if valid_mask.any():
                    idx = valid_mask.idxmax()
                    sample_values.append((dates[idx], closes[idx]))
        else:
            # Standard: Dates in Col 0, OHLC in other columns
            # Find the header row to know which column is CLOSE
            header_row_idx = -1
            for i in range(min(15, len(df))):
                row_vals = [str(val).upper().strip() for val in df.iloc[i].values]
                if "OPEN" in row_vals and "CLOSE" in row_vals:
                    header_row_idx = i
                    break
            
            if header_row_idx != -1:
                headers = [str(val).upper().strip() for val in df.iloc[header_row_idx].values]
                close_col_idx = headers.index("CLOSE")
                # Count valid numeric closes in that column
                closes = pd.to_numeric(df.iloc[header_row_idx+1:, close_col_idx], errors='coerce')
                dates = pd.to_datetime(df.iloc[header_row_idx+1:, 0], errors='coerce')
                valid_mask = closes.notna() & dates.notna()
                total_valid_rows += valid_mask.sum()
                
                if valid_mask.any():
                    idx = valid_mask.idxmax()
                    sample_values.append((dates[idx], closes[idx]))
                    
    return total_valid_rows, sample_values

def main():
    years = range(2019, 2027)
    results = []
    
    print("Verification of Lossless Conversion:")
    print("-" * 60)
    print(f"{'Year':<6} | {'Excel Rows':<12} | {'CSV Rows':<10} | {'Status':<10}")
    print("-" * 60)
    
    for year in years:
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if not matches:
            continue
            
        excel_file = matches[0]
        csv_file = f"data/unified_{year}_bap.csv"
        
        # Get Excel Count
        ex_count, samples = count_excel_rows(excel_file)
        
        # Get CSV Count
        csv_df = pd.read_csv(csv_file)
        csv_count = len(csv_df)
        csv_df['Date'] = pd.to_datetime(csv_df['Date'])
        
        status = "OK" if ex_count == csv_count else f"DIFF ({csv_count - ex_count:+})"
        
        # Spot check
        mismatch = False
        for s_date, s_close in samples:
            match_row = csv_df[csv_df['Date'] == s_date]
            if match_row.empty or abs(match_row.iloc[0]['Close'] - s_close) > 0.0001:
                mismatch = True
                break
        
        if mismatch:
            status = "VALUE ERROR"
            
        print(f"{year:<6} | {ex_count:<12} | {csv_count:<10} | {status:<10}")
        
    print("-" * 60)
    print("Verification complete.")

if __name__ == "__main__":
    main()
