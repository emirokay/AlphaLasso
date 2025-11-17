"""
Instructions
Please write a python script that downloads data from the AlphaLasso database and computes some aggregate measures.
To download the data please use the provided "Advanced Search" (https://alphalasso.cent.uw.edu.pl/advsearch/) which can
be turned into an API by changing the output from "Show results" to "Download TSV".

1. When performing the search please filter on
Lasso type: L4;L5;L6;L7;L8
AND
pLDDT_chain >= 80

The pLDDT_chain is the measure (from 0 to 100) of confidence of the AlphaFold protein prediction model for the whole protein.

2. Choose "Download TSV" instead of "Show results"
3. Customize the result columns by adding the following ones:
Loop_area
Loop_length

This search can take several seconds to complete and should yield 16651 results.

4. Once downloaded this data is provided as a TSV file, so please read it and compute:
a) overall average of the 2 added columns (Loop_area, Loop_length) and the pLDDT_chain
b) averages of the same columns but for each Lasso type (L4, L5, L6, L7, L8) ignoring the different subtypes. i.e. L+4N, L-4C... become just L4 L+5N, L-5N, L+5C, L-5C just L5 etc.

5. Please write the output (results) to screen but also to a file "lasso_proteins_stats.csv" and attach the file along the code when you submit these results.
"""

import statistics
import csv
import requests
import os

# === File Setup ===
FILE_PATH = "alphalasso_results.tsv"
OUTPUT_FILE = "lasso_proteins_stats.csv"

# API URL without the unsupported 'Bridge' column
url = (
    "https://alphalasso.cent.uw.edu.pl/browse?"
    "field=Lasso_type&val=L4%3BL5%3BL6%3BL7%3BL8"
    "&conj=AND"
    "&field=pLDDT_chain&val=%3E%3D80"
    "&raw=2"
    "&result_cols=Lasso_type%3BCategory%3BUniprot%3BOrganism%3BpLDDT_chain%3BProtein_name%3BLoop_area%3BLoop_length"
)

# Download file if it doesn't exist
if not os.path.exists(FILE_PATH):
    print(f"{FILE_PATH} doesn't exist, downloading...")
    response = requests.get(url)
    response.raise_for_status()
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Downloaded {FILE_PATH}")
else:
    print(f"File {FILE_PATH} exists, using local copy")

# === Read and parse TSV ===
with open(FILE_PATH, "r") as f:
    lines = f.read().splitlines()

# Skip header and parse rows
arr = [line.split("\t") for line in lines[1:]]
print(f"{len(arr)} rows scanned")

# === Initialize containers ===
all_areas = []
all_lengths = []
all_plddts = []
lasso_groups = {str(i): [] for i in range(4, 9)}  # L4–L8 groups

# === Process rows safely ===
for item in arr:
    if len(item) < 7:  # Skip malformed rows
        continue
    try:
        lasso_type_full = item[0]
        plddt = float(item[4])
        area = float(item[6])
        length = float(item[7])
    except ValueError:
        continue  # Skip rows with non-numeric values

    all_areas.append(area)
    all_lengths.append(length)
    all_plddts.append(plddt)

    # Group by main Lasso type (L4–L8)
    for key in lasso_groups:
        if key in lasso_type_full:
            lasso_groups[key].append({
                "area": area,
                "length": length,
                "plddt": plddt
            })
            break  # Once matched, stop checking other groups

# === Helper function to calculate averages ===
def calc_avg(arr):
    """Calculate mean values for area, length, and pLDDT in an array of dicts."""
    if not arr:
        return {"area": 0.0, "length": 0.0, "plddt": 0.0}
    return {
        "area": round(statistics.mean(d["area"] for d in arr), 3),
        "length": round(statistics.mean(d["length"] for d in arr), 3),
        "plddt": round(statistics.mean(d["plddt"] for d in arr), 3)
    }

# === Compute results ===
results = []

# Global averages
results.append({"text": "Average Loop area", "value": round(statistics.mean(all_areas), 3)})
results.append({"text": "Average Loop length", "value": round(statistics.mean(all_lengths), 3)})
results.append({"text": "Average Loop area + length", "value": round(statistics.mean(all_areas + all_lengths), 3)})
results.append({"text": "Average pLDDT_chain", "value": round(statistics.mean(all_plddts), 3)})

# Averages by Lasso type
for key in sorted(lasso_groups.keys()):
    avg = calc_avg(lasso_groups[key])
    results.append({"text": f"L{key} Lasso area", "value": avg["area"]})
    results.append({"text": f"L{key} Lasso length", "value": avg["length"]})
    results.append({"text": f"L{key} Lasso pLDDT", "value": avg["plddt"]})

# Print results to screen
for row in results:
    print(f"{row['text']}: {row['value']}")

# Write results to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["text", "value"]
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Results saved to {OUTPUT_FILE}")
