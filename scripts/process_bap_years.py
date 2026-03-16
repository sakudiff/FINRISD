import pandas as pd
import os
import glob

def process_bap_file(input_path, output_path):
    print(f"Loading {input_path}...")
    xl = pd.ExcelFile(input_path)
    
    combined_data = []
    
    for sheet_name in xl.sheet_names:
        print(f"  Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Detection logic for transposed vs standard
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            # Transpose
            df = df.T
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        else:
            # Standard
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
            
        # Clean up column names
        new_cols = {}
        for col in df.columns:
            c_str = str(col).upper().strip()
            if 'OPEN' in c_str: new_cols[col] = 'Open'
            elif 'HIGH' in c_str: new_cols[col] = 'High'
            elif 'LOW' in c_str: new_cols[col] = 'Low'
            elif 'CLOSE' in c_str: new_cols[col] = 'Close'
        
        df.rename(columns=new_cols, inplace=True)
        
        # Filter for only OHLC + Date
        cols_to_keep = ['Date', 'Open', 'High', 'Low', 'Close']
        existing_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[existing_cols]
        
        # Drop invalid dates and rows where all OHLC are NaN
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        # Ensure numeric values
        for val_col in ['Open', 'High', 'Low', 'Close']:
            if val_col in df.columns:
                df[val_col] = pd.to_numeric(df[val_col], errors='coerce')
        
        df = df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all')
        
        combined_data.append(df)
    
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
    years = [2020, 2021, 2022, 2023]
    for year in years:
        # Match files starting with year
        pattern = f"data/{year} BAP*.xlsx"
        matches = glob.glob(pattern)
        if matches:
            input_file = matches[0]
            output_file = f"data/unified_{year}_bap.csv"
            process_bap_file(input_file, output_file)
        else:
            print(f"No file found for year {year} matching {pattern}")

if __name__ == "__main__":
    main()
