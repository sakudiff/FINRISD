"""
Master BAP FX Unification Engine.
Aggregates yearly CSVs into a single master record with strict overlap validation.
"""

import glob
import os
from typing import List, Set

import pandas as pd


def check_integrity(df_master: pd.DataFrame, df_new: pd.DataFrame, source_label: str) -> None:
    """
    Validates schema and data consistency between the master record and new data.
    
    Args:
        df_master: The existing master DataFrame.
        df_new: The new yearly DataFrame to be integrated.
        source_label: Identifier for the source file (for logging).
        
    Raises:
        ValueError: If schema mismatch or data contradiction is detected.
    """
    # Schema validation
    if not df_master.columns.equals(df_new.columns):
        raise ValueError(f"Schema mismatch in {source_label}! Master: {df_master.columns}, New: {df_new.columns}")
    
    # Overlap and consistency check
    common_dates: Set[str] = set(df_master['Date']).intersection(set(df_new['Date']))
    if common_dates:
        print(f"  [INFO] Found {len(common_dates)} overlapping dates in {source_label}.")
        for date_str in sorted(list(common_dates)):
            master_close = df_master[df_master['Date'] == date_str].iloc[0]['Close']
            new_close = df_new[df_new['Date'] == date_str].iloc[0]['Close']
            
            # Allow for floating point epsilon
            if abs(master_close - new_close) > 1e-5:
                raise ValueError(f"CRITICAL: Value contradiction on {date_str} in {source_label}. "
                                 f"Master={master_close}, New={new_close}")


def main() -> None:
    """Orchestrates the unification of all yearly BAP CSVs."""
    csv_files = sorted(glob.glob("data/unified/unified_20*_bap.csv"))
    if not csv_files:
        print("[ERROR] No source CSVs found in data/unified/. Run extraction scripts first.")
        return

    print("Executing master unification...")
    
    # Initialize master with the first available year
    master_df = pd.read_csv(csv_files[0])
    master_df['Date'] = pd.to_datetime(master_df['Date']).dt.strftime('%Y-%m-%d')
    print(f"Initialized with {os.path.basename(csv_files[0])} ({len(master_df)} records)")

    for file_path in csv_files[1:]:
        source_name = os.path.basename(file_path)
        current_df = pd.read_csv(file_path)
        current_df['Date'] = pd.to_datetime(current_df['Date']).dt.strftime('%Y-%m-%d')
        
        print(f"Integrating {source_name}...")
        
        # Verify integrity before merging
        check_integrity(master_df, current_df, source_name)
        
        initial_size = len(master_df)
        master_df = pd.concat([master_df, current_df], ignore_index=True)
        
        # Deduplicate and sort O(N log N)
        master_df = master_df.drop_duplicates(subset=['Date']).sort_values('Date')
        
        final_size = len(master_df)
        print(f"  Merged records. Growth: {initial_size} -> {final_size} (+{final_size - initial_size})")

    output_path = "data/unified/unified_bap_master.csv"
    master_df.to_csv(output_path, index=False)
    
    print("\nUNIFICATION COMPLETE")
    print(f"Destination: {output_path}")
    print(f"Temporal Span: {master_df['Date'].min()} to {master_df['Date'].max()}")
    print(f"Total Trading Days: {len(master_df)}")


if __name__ == "__main__":
    main()
