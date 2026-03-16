import pandas as pd
import os
import glob

def process_bap_standard(input_path, output_path):
    print(f"Loading {input_path}...")
    xl = pd.ExcelFile(input_path)
    
    combined_data = []
    
    for sheet_name in xl.sheet_names:
        print(f"  Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Find header row
        header_row_idx = -1
        for i in range(min(10, len(df))):
            row_vals = [str(val).upper().strip() for val in df.iloc[i].values]
            if "OPEN" in row_vals and "HIGH" in row_vals:
                header_row_idx = i
                break
        
        if header_row_idx == -1:
            print(f"    Header row not found in {sheet_name}. Skipping.")
            continue
            
        # Map columns
        headers = [str(val).upper().strip() for val in df.iloc[header_row_idx].values]
        col_map = {}
        for idx, h in enumerate(headers):
            if "OPEN" == h: col_map[idx] = "Open"
            elif "HIGH" == h: col_map[idx] = "High"
            elif "LOW" == h: col_map[idx] = "Low"
            elif "CLOSE" == h: col_map[idx] = "Close"
        
        # Column 0 is expected to be Date for 2024-2026
        date_col_idx = 0
        
        data_df = df.iloc[header_row_idx + 1:].copy()
        
        # Extract rows
        rows = []
        for _, row in data_df.iterrows():
            # Parse Date
            dt = pd.to_datetime(row[date_col_idx], errors='coerce')
            if pd.isna(dt):
                continue
            
            try:
                # Extract OHLC
                row_data = {"Date": dt}
                valid_ohlc = True
                for idx, name in col_map.items():
                    val = pd.to_numeric(row[idx], errors='coerce')
                    if pd.isna(val):
                        valid_ohlc = False
                        break
                    row_data[name] = float(val)
                
                if valid_ohlc:
                    rows.append(row_data)
            except:
                continue
        
        if rows:
            combined_data.append(pd.DataFrame(rows))
    
    if not combined_data:
        print(f"  No data extracted from {input_path}!")
        return
        
    unified_df = pd.concat(combined_data, ignore_index=True)
    unified_df = unified_df.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Invariant Fix: High must be >= Low
    swapped = (unified_df['High'] < unified_df['Low'])
    if swapped.any():
        print(f"  Fixing {swapped.sum()} rows where High < Low")
        unified_df.loc[swapped, ['High', 'Low']] = unified_df.loc[swapped, ['Low', 'High']].values
    
    unified_df.to_csv(output_path, index=False)
    print(f"Success. Unified data saved to {output_path}")

def main():
    years = [2024, 2025, 2026]
    for year in years:
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if matches:
            input_file = matches[0]
            output_file = f"data/unified_{year}_bap.csv"
            process_bap_standard(input_file, output_file)
        else:
            print(f"No file found for year {year} matching {pattern}")

if __name__ == "__main__":
    main()
