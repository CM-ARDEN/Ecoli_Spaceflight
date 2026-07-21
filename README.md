# E. coli Spaceflight Gene Expression & DEG Pipeline

This repository contains an end-to-end bioinformatics and transcriptomics data processing pipeline designed to analyze differential gene expression (DEG) in Escherichia coli under simulated spaceflight/microgravity stress conditions.

---

## Overview

Spaceflight environments expose microorganisms to microgravity and cosmic radiation, inducing significant physiological and transcriptional alterations. This project downloads raw RNA-Seq/count data, performs normalization (CPM), identifies differentially expressed genes (DEGs), and visualizes significant transcriptional shifts using a **Volcano Plot**.

---

## Repository Structure

```text
Ecoli_Spaceflight/
│
├── data/                       # Contains processed counts, metadata, DEG results & plots
│   └── volcano_plot.png        # Generated volcano plot
├── notebook/                   # Exploratory analysis & Jupyter Notebooks
├── 01_data_download.py         # Script to fetch raw dataset and metadata
├── 02_data_analysis.py         # Quality control & normalization (CPM)
├── 03_diff_expression.py       # Differential Expression Analysis (DEG calculations)
└── 04_visualization.py         # Volcano plot generator (Matplotlib / Seaborn)
