# FINRISD: BAP FX Data Extraction & Unification Pipeline

The extraction of financial data from disparate, legacy Excel summaries is an exercise in archaeological precision. This repository provides a robust, $O(n)$ pipeline for normalizing Bankers Association of the Philippines (BAP) FX historical data spanning 2019 to 2026. It transforms inconsistent, often transposed spreadsheet layouts into a strictly schema-compliant master dataset.

## Architecture

The pipeline is decoupled by year-range to handle evolving Excel formats and layout heuristics.

1.  **Extraction Stage**: Year-specific engines scan raw Excel files, detect transposed vs. standard layouts, and extract OHLC (Open, High, Low, Close) features.
2.  **Sanitization Stage**: Automated reconciliation of temporal gaps and invariant verification (e.g., ensuring $High \ge Low$).
3.  **Unification Stage**: A master engine aggregates yearly records, performing strict overlap integrity checks to prevent data contradiction.

## Directory Structure

```text
FINRISD/
├── data/                       # Raw source Excel files (2019-2026)
│   └── unified/                # Destination for normalized CSV outputs
├── scripts/
│   ├── process_2019_bap.py     # Special handling for 2019 legacy layouts
│   ├── process_bap_years.py    # Extraction engine for 2020-2023
│   ├── process_bap_recent.py   # Extraction engine for 2024-2026
│   ├── master_unification.py   # Aggregates all years into a master record
│   ├── analyze_gaps.py        # Audits data for missing trading days
│   └── verify_lossless.py      # Cross-references CSV results with Excel sources
└── README.md                   # This clinical guide
```

## Execution Protocol

To replicate the dataset from scratch, execute the following sequence. Ensure all raw `.xlsx` files are present in the `data/` directory.

### 1. Year-Specific Extraction
Run the extraction scripts to generate intermediate yearly CSVs in `data/unified/`.

```bash
uv run scripts/process_2019_bap.py
uv run scripts/process_bap_years.py
uv run scripts/process_bap_recent.py
```

### 2. Verification & Gap Analysis
Before unification, audit the integrity of the extracted records.

```bash
uv run scripts/verify_lossless.py
uv run scripts/analyze_gaps.py
```

### 3. Master Unification
Merge all verified yearly records into the final master dataset.

```bash
uv run scripts/master_unification.py
```

## Technical Specifications

- **Complexity**: All extraction engines operate in $O(n)$ where $n$ is the number of records per sheet. Unification performs an $O(n \log n)$ sort to ensure temporal consistency.
- **Dependencies**: 
  - `pandas`: Data manipulation and Excel parsing.
  - `openpyxl`: Backend for `.xlsx` I/O.
- **Invariants**: 
  - Date uniqueness is enforced via `drop_duplicates(subset=['Date'])`.
  - Feature integrity is enforced via `High = max(High, Low)`.
  - All output dates follow the ISO 8601 standard (`YYYY-MM-DD`).

## Audit

The `verify_lossless.py` script performs a cell-by-cell comparison of random samples between the source Excel and the generated CSV. Any delta in record count or value mismatch will trigger a `VAL MISMATCH` or `DELTA` status. Success implies zero loss of information during the normalization process.

---

*Note: This repository focuses on the data engineering layer. For the analytical R-Markdown and HTML visualizations, refer to website [link here](https://valueatrisk.netlify.app/#section-4-item-1-close-to-close-var-95-one-tail) .*
