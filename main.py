#!/usr/bin/env python3
"""
Oura Sleep CSV Cleaner and Flattener

This script processes Oura Ring daily sleep exports (CSV), which use
semicolon delimiters and contain malformed JSON-like data in the 'contributors'
column. It performs the following steps:

  - Changes into the configured working directory
  - Loads and inspects the CSV
  - Parses and normalizes the contributors field via regex
  - Expands contributor metrics into their own columns
  - Outputs a flattened, analysis-ready CSV

Date: 2025-11-04
"""

import os
import re
import json
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Working directory and filenames
WORKDIR = Path("/home/cporter/Downloads/")
INPUT_FILE = WORKDIR / "dailysleep.csv"
OUTPUT_FILE = WORKDIR / "dailysleep_flat.csv"

# ---------------------------------------------------------------------------
# Helper Function
# ---------------------------------------------------------------------------

def clean_contributors(raw_str: str) -> dict:
    """
    Parse malformed Oura 'contributors' strings into a dictionary.

    Oura exports this field as:
        {"deep_sleep": 78  "efficiency": 81 "latency": 89 "rem_sleep": 76 ...}

    which is invalid JSON (missing commas). Instead of attempting to fix JSON,
    we extract key–value pairs directly using regex.

    Returns:
        dict: {metric_name: value, ...}
    """
    if pd.isna(raw_str):
        return {}

    s = str(raw_str).strip()

    # Extract key–value pairs like "efficiency": 81
    matches = re.findall(r'"?([a-zA-Z_]+)"?\s*:\s*([0-9.]+)', s)

    if not matches:
        print(f"[WARN] No key-value pairs found in: {s[:80]}...")
        return {}

    # Convert numeric strings to int/float
    return {k: float(v) if '.' in v else int(v) for k, v in matches}

# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def main():
    """Main execution pipeline for Oura data cleanup."""
    print(f"[INFO] Current directory: {os.getcwd()}")
    os.chdir(WORKDIR)
    print(f"[INFO] Changed directory to: {os.getcwd()}")

    # --- Load CSV ---
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"[ERROR] Input file not found: {INPUT_FILE}")

    print(f"[INFO] Loading CSV: {INPUT_FILE.name}")
    df = pd.read_csv(INPUT_FILE, sep=';')
    print(f"[INFO] Loaded {len(df)} rows with columns: {list(df.columns)}")

    # --- Parse and expand contributors ---
    print("[INFO] Parsing 'contributors' column...")
    df["contributors_dict"] = df["contributors"].apply(clean_contributors)

    print("[INFO] Expanding contributor metrics...")
    contributors_expanded = pd.json_normalize(df["contributors_dict"])
    contributors_expanded.columns = [
        f"contributors_{c}" for c in contributors_expanded.columns
    ]

    # Merge flattened data with original frame
    df_flat = pd.concat(
        [df.drop(columns=["contributors", "contributors_dict"]),
         contributors_expanded],
        axis=1
    )

    # --- Save output ---
    df_flat.to_csv(OUTPUT_FILE, index=False)
    print(f"[INFO] Flattened dataset written to: {OUTPUT_FILE.resolve()}")

    # --- Inspect ---
    print("[INFO] Sample output:")
    print(df_flat.head())
    print("[INFO] Column data types:")
    print(df_flat.dtypes)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
        print("[INFO] Script completed successfully")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        raise

