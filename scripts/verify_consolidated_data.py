import pandas as pd
import glob
import os

def main():
    csv_files = sorted(glob.glob("data/unified_20*_bap.csv"))
    dfs = []
    
    for f in csv_files:
        dfs.append(pd.read_csv(f))
    
    master_df = pd.concat(dfs, ignore_index=True)
    master_df['Date'] = pd.to_datetime(master_df['Date'])
    
    # Drop exact duplicates if they exist across files
    initial_count = len(master_df)
    master_df = master_df.sort_values('Date').drop_duplicates(subset=['Date'])
    final_count = len(master_df)
    
    print(f"Total rows collected: {initial_count}")
    print(f"Total unique rows: {final_count}")
    print(f"Duplicates removed: {initial_count - final_count}")
    
    master_df['Year'] = master_df['Date'].dt.year
    master_df['Month'] = master_df['Date'].dt.month
    
    # Group by Year and Month
    monthly_summary = master_df.groupby(['Year', 'Month']).agg(
        days=('Date', 'count'),
        start=('Date', 'min'),
        end=('Date', 'max'),
        price_avg=('Close', 'mean')
    ).reset_index()
    
    # Convert to string for display
    monthly_summary['start'] = monthly_summary['start'].dt.strftime('%Y-%m-%d')
    monthly_summary['end'] = monthly_summary['end'].dt.strftime('%Y-%m-%d')
    monthly_summary['price_avg'] = monthly_summary['price_avg'].round(3)
    
    print("\n--- GLOBAL MONTHLY SUMMARY ---")
    # Show the first 24 and last 12 for brevity if it's too long, 
    # but the user asked to go through "each year", so I'll print the whole thing.
    # It should be ~8 years * 12 months = 96 rows.
    pd.set_option('display.max_rows', None)
    print(monthly_summary.to_string(index=False))
    
    # Check for gaps (months with very few rows)
    gaps = monthly_summary[monthly_summary['days'] < 15]
    if not gaps.empty:
        print("\n[!] WARNING: Potential gaps found (months with < 15 days):")
        print(gaps.to_string(index=False))
    else:
        print("\n[+] Coverage looks solid (all months have >= 15 days).")

if __name__ == "__main__":
    main()
