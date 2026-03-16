import pandas as pd
import os

def main():
    # Load our master (Raw Trading Days)
    our_master = pd.read_csv("data/unified/unified_bap_master.csv")
    our_master['Date'] = pd.to_datetime(our_master['Date'])
    
    # Load the other file
    other_file = "data/unified_usdphp_bap.csv"
    if not os.path.exists(other_file):
        print(f"Error: {other_file} not found.")
        return
        
    other_df = pd.read_csv(other_file)
    other_df['Date'] = pd.to_datetime(other_df['Date'])
    
    print(f"Our Master Rows: {len(our_master)}")
    print(f"Other File Rows: {len(other_df)}")
    
    # Check if 'other' has non-trading days (weekends)
    other_df['Is_Weekend'] = other_df['Date'].dt.dayofweek >= 5
    weekends_in_other = other_df[other_df['Is_Weekend']]
    print(f"Weekends found in other file: {len(weekends_in_other)}")
    
    # Check for forward-filling logic in 'other'
    # Pick a few weekends and see if they match the previous Friday
    sample_weekend = weekends_in_other.iloc[0]['Date']
    friday = sample_weekend - pd.Timedelta(days=(sample_weekend.dayofweek - 4))
    
    val_friday = other_df[other_df['Date'] == friday]['Close'].values
    val_weekend = other_df[other_df['Date'] == sample_weekend]['Close'].values
    
    if len(val_friday) > 0 and len(val_weekend) > 0:
        if abs(val_friday[0] - val_weekend[0]) < 0.0001:
            print(f"Confirmed: Other file repeats Friday values ({friday.date()}) into weekends ({sample_weekend.date()}).")

    # Check for "made up" values: Are there any dates in our master that have DIFFERENT values in the other file?
    merged = pd.merge(our_master, other_df, on='Date', suffixes=('_ours', '_other'))
    mismatches = merged[abs(merged['Close_ours'] - merged['Close_other']) > 0.001]
    
    if not mismatches.empty:
        print(f"\n[!] WARNING: Found {len(mismatches)} price mismatches on actual trading days!")
        print(mismatches[['Date', 'Close_ours', 'Close_other']].head(10))
    else:
        print("\n[+] Integrity Check: All values match on published trading days.")

if __name__ == "__main__":
    main()
