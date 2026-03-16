import pandas as pd
import glob
import os

def analyze_missing_business_days(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    
    # Generate all business days in that range (Monday-Friday)
    all_b_days = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Find which business days are NOT in our dataframe
    missing_days = all_b_days.difference(df['Date'])
    
    return len(all_b_days), len(missing_days), missing_days

def main():
    csv_files = sorted(glob.glob("data/unified/unified_20*_bap.csv"))
    
    print(f"{'Year':<6} | {'B-Days (M-F)':<12} | {'Missing Days':<15} | {'Missing %':<10}")
    print("-" * 55)
    
    for f in csv_files:
        year = os.path.basename(f).split('_')[1]
        total_b, missing_count, missing_list = analyze_missing_business_days(f)
        
        pct = (missing_count / total_b) * 100
        print(f"{year:<6} | {total_b:<12} | {missing_count:<15} | {pct:<10.2f}%")
        
        if missing_count > 0:
            samples = ", ".join([d.strftime('%m-%d') for d in missing_list[:8]])
            print(f"  Gaps: {samples}...")

if __name__ == "__main__":
    main()
