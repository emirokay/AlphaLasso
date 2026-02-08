# AlphaLasso Data Analysis Pipeline

## Overview
This project provides a Python-based automation tool to interface with the [AlphaLasso database](https://alphalasso.cent.uw.edu.pl/), a specialized resource for identifying and analyzing "lassos"—topologically complex structures in proteins predicted by AlphaFold.

The script programmatically queries the database, downloads structural metadata, and performs statistical aggregation on key geometric metrics to understand the physical properties of these unique protein folds.



## Project Objectives
The goal of this analysis is to compare the physical characteristics of different lasso configurations (L4 through L8). The pipeline is designed to:
* **Filter for High-Confidence Structures:** Only processes entries with a `pLDDT_chain` score $\ge$ 80.
* **Extract Geometric Data:** Focuses on `Loop Area` and `Loop Length`.
* **Standardize Lasso Categorization:** Aggregates various subtypes (e.g., $L+4N$, $L-4C$) into their primary parent groups ($L4, L5, L6, L7, L8$) for broader statistical significance.

## Technical Features
* **Automated Data Retrieval:** Uses the `requests` library to interface with the AlphaLasso "Advanced Search" converted into a TSV API.
* **Data Parsing:** Efficiently handles large-scale datasets (approx. 16,000+ records).
* **Statistical Analysis:** * Computes global means for structural metrics.
    * Generates specific averages for each Lasso class using Python's `statistics` module.
* **Output Generation:** Exports results to both the terminal and a formatted `lasso_proteins_stats.csv` file.
