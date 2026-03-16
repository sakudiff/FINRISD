import pandas as pd
import os
import glob

def inspect_files():
    files = sorted(glob.glob("data/*.xlsx"))
    results = {}
    for f in files:
        try:
            xl = pd.ExcelFile(f)
            results[os.path.basename(f)] = {
                "sheets": xl.sheet_names,
                "head": pd.read_excel(f, sheet_name=xl.sheet_names[0], nrows=10).to_json()
            }
        except Exception as e:
            results[os.path.basename(f)] = {"error": str(e)}
    return results

if __name__ == "__main__":
    import json
    print(json.dumps(inspect_files(), indent=2))
