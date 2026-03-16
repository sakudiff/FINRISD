import pandas as pd
import glob
import os
from datetime import datetime

def extract_from_sheet(df, sheet_name):
    data = []
    header_row_idx = -1
    for i in range(min(15, len(df))):
        row_vals = [str(x).upper().strip() for x in df.iloc[i].values]
        if "OPEN" in row_vals and "HIGH" in row_vals:
            header_row_idx = i
            break
    
    if header_row_idx != -1:
        headers = [str(x).upper().strip() for x in df.iloc[header_row_idx].values]
        col_map = {}
        for idx, h in enumerate(headers):
            if "OPEN" == h: col_map[idx] = "Open"
            elif "HIGH" == h: col_map[idx] = "High"
            elif "LOW" == h: col_map[idx] = "Low"
            elif "CLOSE" == h: col_map[idx] = "Close"
            elif "FROM" in h or "DATE" in h: col_map[idx] = "Date"
        
        if "Date" not in col_map.values():
            if header_row_idx > 0:
                prev_row = [str(x).upper().strip() for x in df.iloc[header_row_idx-1].values]
                for idx, h in enumerate(prev_row):
                    if "FROM" in h or "DATE" in h: col_map[idx] = "Date"
            if "Date" not in col_map.values():
                for c_idx in [0, 1]:
                    peek = pd.to_datetime(df.iloc[header_row_idx+1:, c_idx], errors='coerce')
                    if peek.notna().sum() > 2:
                        col_map[c_idx] = "Date"
                        break
        
        if "Date" in col_map.values() and "Open" in col_map.values():
            data_df = df.iloc[header_row_idx+1:].copy()
            d_idx = next(k for k,v in col_map.items() if v == "Date")
            o_idx = next(k for k,v in col_map.items() if v == "Open")
            h_idx = next(k for k,v in col_map.items() if v == "High")
            l_idx = next(k for k,v in col_map.items() if v == "Low")
            c_idx = next(k for k,v in col_map.items() if v == "Close")
            
            for _, row in data_df.iterrows():
                dt = pd.to_datetime(row[d_idx], errors='coerce')
                if pd.isna(dt) or dt.year < 2018: continue
                try:
                    data.append({
                        "Date": dt,
                        "Open": float(row[o_idx]),
                        "High": float(row[h_idx]),
                        "Low": float(row[l_idx]),
                        "Close": float(row[c_idx])
                    })
                except: continue
            return data

    label_col = -1
    for c in range(min(3, df.shape[1])):
        col_vals = [str(x).upper().strip() for x in df.iloc[:, c].values]
        if "OPEN" in col_vals and "HIGH" in col_vals:
            label_col = c
            break
    
    if label_col != -1:
        field_map = {}
        for i in range(len(df)):
            val = str(df.iloc[i, label_col]).upper().strip()
            if val == "OPEN": field_map['Open'] = i
            elif val == "HIGH": field_map['High'] = i
            elif val == "LOW": field_map['Low'] = i
            elif val == "CLOSE": field_map['Close'] = i
        
        date_row = -1
        for i in range(min(5, len(df))):
            if i in field_map.values(): continue
            row_dates = pd.to_datetime(df.iloc[i, label_col+1:], errors='coerce')
            if row_dates.notna().sum() > 2:
                date_row = i
                break
        
        if date_row != -1:
            for col in range(label_col + 1, df.shape[1]):
                dt = pd.to_datetime(df.iloc[date_row, col], errors='coerce')
                if pd.isna(dt) or dt.year < 2018: continue
                try:
                    data.append({
                        "Date": dt,
                        "Open": float(df.iloc[field_map['Open'], col]),
                        "High": float(df.iloc[field_map['High'], col]),
                        "Low": float(df.iloc[field_map['Low'], col]),
                        "Close": float(df.iloc[field_map['Close'], col])
                    })
                except: continue
            return data
    return []

def parse_bap_file(file_path):
    print(f"Processing {file_path}...")
    xl = pd.ExcelFile(file_path)
    file_data = []
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        sheet_data = extract_from_sheet(df, sheet_name)
        file_data.extend(sheet_data)
    return file_data

def main():
    files = sorted(glob.glob("data/*.xlsx"))
    master_data = []
    for f in files:
        master_data.extend(parse_bap_file(f))
    
    if not master_data:
        print("No data extracted!")
        return

    df = pd.DataFrame(master_data)
    df = df.drop_duplicates(subset=['Date']).sort_values('Date')
    
    # Invariants Fix
    swapped = (df['High'] < df['Low'])
    df.loc[swapped, ['High', 'Low']] = df.loc[swapped, ['Low', 'High']].values

    # Step: Ensure every year, month, and day is present (Gap Imputation)
    start_date = pd.Timestamp("2019-01-01") # Mandated start
    end_date = pd.Timestamp("2026-02-27")   # Mandated cutoff
    full_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    df = df.set_index('Date').reindex(full_range)
    
    # Forward-fill gaps (weekends/holidays)
    # Price stays constant if no trading occurred
    df = df.ffill().bfill() # bfill handles Jan 1 if missing
    
    df.index.name = 'Date'
    df = df.reset_index()
    
    # Formatting
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    output_path = "data/unified_usdphp_bap.csv"
    df.to_csv(output_path, index=False)
    print(f"Success. Consolidated {len(df)} rows (every calendar day from {start_date.date()} to {end_date.date()}) to {output_path}")

if __name__ == "__main__":
    main()
