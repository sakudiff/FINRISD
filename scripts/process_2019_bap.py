import pandas as pd
import os

def process_2019_bap(input_path, output_path):
    print(f"Loading {input_path}...")
    xl = pd.ExcelFile(input_path)
    
    combined_data = []
    
    for sheet_name in xl.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
        # Detection logic
        # If the first row has many dates and the first column has labels like 'TIME', 'OPEN'
        # it's transposed.
        
        # Peek at first row (excluding first cell)
        first_row_dates = pd.to_datetime(df.iloc[0, 1:], errors='coerce')
        # Peek at first column (excluding first cell)
        first_col_dates = pd.to_datetime(df.iloc[1:, 0], errors='coerce')
        
        is_transposed = first_row_dates.notna().sum() > first_col_dates.notna().sum()
        
        if is_transposed:
            print(f"  Detected transposed layout for {sheet_name}. Transposing...")
            # Transpose the dataframe
            df = df.T
            # After transpose:
            # Row 0 has the labels (TIME, OPEN, HIGH, LOW, CLOSE...)
            # Column 0 has the dates
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            # The dates were in the 'header' which is now in a column. 
            # In the original transposed Excel, the dates were in the first row.
            # After df.T, they are in the index if we didn't use header=None, 
            # but we used header=None, so they are in Row 0 of the original df.
            # Thus after df.T they are in Column 0.
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        else:
            print(f"  Detected standard layout for {sheet_name}.")
            # Assume Row 0 is header
            df.columns = df.iloc[0]
            df = df.drop(df.index[0])
            # Assume Col 0 is Date
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
            
        # Clean up column names to be consistent
        new_cols = {}
        for col in df.columns:
            c_str = str(col).upper().strip()
            if 'OPEN' in c_str: new_cols[col] = 'Open'
            elif 'HIGH' in c_str: new_cols[col] = 'High'
            elif 'LOW' in c_str: new_cols[col] = 'Low'
            elif 'CLOSE' in c_str: new_cols[col] = 'Close'
            elif 'DATE' in c_str or c_str == 'NAN' or c_str == '': pass # Date already handled or empty
        
        df.rename(columns=new_cols, inplace=True)
        
        # Filter for only OHLC + Date
        cols_to_keep = ['Date', 'Open', 'High', 'Low', 'Close']
        # Check if they exist
        existing_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[existing_cols]
        
        # Drop rows where Date is invalid
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        # Ensure numeric values
        for val_col in ['Open', 'High', 'Low', 'Close']:
            if val_col in df.columns:
                df[val_col] = pd.to_numeric(df[val_col], errors='coerce')
        
        # Drop rows where all OHLC are NaN (empty trading days or metadata)
        df = df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all')
        
        combined_data.append(df)
    
    if not combined_data:
        print("No data extracted!")
        return
        
    unified_df = pd.concat(combined_data, ignore_index=True)
    unified_df = unified_df.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Invariant Fix: High must be >= Low
    swapped = (unified_df['High'] < unified_df['Low'])
    if swapped.any():
        print(f"  Fixing {swapped.sum()} rows where High < Low")
        unified_df.loc[swapped, ['High', 'Low']] = unified_df.loc[swapped, ['Low', 'High']].values
    
    unified_df.to_csv(output_path, index=False)
    print(f"Success. Unified 2019 data saved to {output_path}")

if __name__ == "__main__":
    input_file = "data/2019 BAP FX Summary.xlsx"
    output_file = "data/unified_2019_bap.csv"
    process_2019_bap(input_file, output_file)
