import pandas as pd
import os
import json
import re
import numpy as np

# Check 
print("Current directory:", os.getcwd())

# Change directory
os.chdir("/home/cporter/Downloads/")

# Confirm the change
print("Now in:", os.getcwd())


# Load the CSV (use ; as delimiter)
df = pd.read_csv("dailysleep.csv", sep=';')


def clean_contributors(raw_str: str) -> dict:
    """
    Parse the malformed Oura 'contributors' field using regex.

    This field looks like:
        {"deep_sleep": 78  "efficiency": 81 "latency": 89 "rem_sleep": 76 ...}
    which is not valid JSON (missing commas). This parser extracts
    key–value pairs directly instead of trying to fix JSON syntax.
    """
    if pd.isna(raw_str):
        return {}

    s = str(raw_str).strip()

    # Find all key-value pairs like "key": 123
    matches = re.findall(r'"?([a-zA-Z_]+)"?\s*:\s*([0-9.]+)', s)

    # Convert to dict
    if not matches:
        print(f"[WARN] No key-value pairs found in: {s[:80]}...")
        return {}

    return {k: float(v) if '.' in v else int(v) for k, v in matches}

# Apply cleaning and parsing
df["contributors_dict"] = df["contributors"].apply(clean_contributors)

contributors_expanded = pd.json_normalize(df["contributors_dict"])
contributors_expanded.columns = [f"contributors_{c}" for c in contributors_expanded.columns]

# Merge back into the main DataFrame
df = pd.concat([df.drop(columns=["contributors", "contributors_dict"]), contributors_expanded], axis=1)


# print(df.dtypes)

# --- EIGENVALUE DECOMPOSITION SECTION ---

# Select only numeric contributor columns
contrib_cols = [c for c in df.columns if c.startswith("contributors_")]
contrib_data = df[contrib_cols].dropna()

print(f"\nUsing {len(contrib_cols)} contributor features for analysis.")

# Compute covariance matrix
cov_matrix = np.cov(contrib_data.T)
print("\nCovariance Matrix Shape:", cov_matrix.shape)

# Perform eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Sort eigenvalues (and corresponding eigenvectors) descending
sorted_idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_idx]
eigenvectors = eigenvectors[:, sorted_idx]

# Compute explained variance ratio
explained_variance_ratio = eigenvalues / np.sum(eigenvalues)

# Display top components
num_top = 3  # Adjust number of top components
print(f"\nTop {num_top} Principal Components by Contribution:\n")

for i in range(num_top):
    print(f"Component {i+1}:")
    print(f"  Eigenvalue: {eigenvalues[i]:.4f}")
    print(f"  Explained Variance: {explained_variance_ratio[i]*100:.2f}%")
    
    # Top contributing features for this component
    component_vector = eigenvectors[:, i]
    contributions = pd.Series(component_vector, index=contrib_cols).abs().sort_values(ascending=False)
    print("  Top Contributing Features:")
    print(contributions.head(5), "\n")

# Optional: Save results to JSON
pca_summary = {
    "eigenvalues": eigenvalues.tolist(),
    "explained_variance_ratio": explained_variance_ratio.tolist(),
    "features": contrib_cols,
}

with open("pca_summary.json", "w") as f:
    json.dump(pca_summary, f, indent=2)

print("\nPCA summary saved to pca_summary.json")

