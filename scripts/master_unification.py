import pandas as pd
import glob
import os

def check_integrity(df_old, df_new, year):
    # Schema check
    if not df_old.columns.equals(df_new.columns):
        raise ValueError(f"Schema mismatch in {year}! Expected {df_old.columns}, got {df_new.columns}")
    
    # Overlap check
    common_dates = set(df_old['Date']).intersection(set(df_new['Date']))
    if common_dates:
        print(f"  [!] Found {len(common_dates)} overlapping dates in {year} data.")
        # Verify values match for common dates
        for d in sorted(list(common_dates)):
            old_val = df_old[df_old['Date'] == d].iloc[0]['Close']
            new_val = df_new[df_new['Date'] == d].iloc[0]['Close']
            if abs(old_val - new_val) > 0.0001:
                print(f"    [CRITICAL] Value mismatch on {d}: Old={old_val}, New={new_val}")
            else:
                print(f"    Overlap date {d} verified: values match.")

def main():
    csv_files = sorted(glob.glob("data/unified/unified_20*_bap.csv"))
    if not csv_files:
        print("No source CSVs found in data/unified/")
        return

    print("Starting master unification one-by-one...")
    
    # Initialize with the first year (2019)
    master_df = pd.read_csv(csv_files[0])
    master_df['Date'] = pd.to_datetime(master_df['Date']).dt.strftime('%Y-%m-%d')
    print(f"Initialized with {os.path.basename(csv_files[0])} ({len(master_df)} rows)")

    for f in csv_files[1:]:
        year_file = os.path.basename(f)
        current_df = pd.read_csv(f)
        current_df['Date'] = pd.to_datetime(current_df['Date']).dt.strftime('%Y-%m-%d')
        
        print(f"Processing {year_file}...")
        
        # Check integrity before merge
        check_integrity(master_df, current_df, year_file)
        
        # Merge
        initial_count = len(master_df)
        new_rows_count = len(current_df)
        
        master_df = pd.concat([master_df, current_df], ignore_index=True)
        
        # Deduplicate and Sort
        master_df = master_df.drop_duplicates(subset=['Date']).sort_values('Date')
        
        final_count = len(master_df)
        print(f"  Merged {new_rows_count} rows. Total rows now: {final_count} (Net change: {final_count - initial_count})")

    output_path = "data/unified/unified_bap_master.csv"
    master_df.to_csv(output_path, index=False)
    print("-" * 50)
    print(f"SUCCESS: Master unified file created at {output_path}")
    print(f"Final dataset spans {master_df['Date'].min()} to {master_df['Date'].max()}")
    print(f"Total trading days: {len(master_df)}")

if __name__ == "__main__":
    main()
