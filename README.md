# Functional Gene Cluster Analysis and Visualization

This repository provides two Python scripts to identify functional gene clusters from DAVID annotation files and to visualize their genomic localization as **smoothed density heatmaps** with significance testing.

[![DOI](https://zenodo.org/badge/1049834575.svg)](https://doi.org/10.5281/zenodo.17047999)


---

## ✨ Features
1. **DAVID TXT → Gene Cluster Excel**
   - Converts DAVID `gene2term` annotation TXT files into Excel files of functional clusters.
   - User-defined keyword groups map to annotation terms (e.g., secretion, virulence, motility).
   - Each group becomes one Excel column listing locus tags that match.

2. **Gene Cluster Heatmap with KS Significance**
   - Reads an Excel file of genome-ordered locus tags and functional clusters.
   - Plots a heatmap showing smoothed gene density along the genome.
   - Applies the Kolmogorov–Smirnov test to assess whether cluster positions deviate significantly from uniform distribution.
   - Annotates each row with cluster size and significance stars (ns, *, **, ***).

---

## 📦 Requirements
Python ≥ 3.9 with:

```
pandas
numpy
matplotlib
scipy
openpyxl
tkinter   # usually included with Python
```

Install with:
```bash
pip install pandas numpy matplotlib scipy openpyxl
```

---

## 📥 Input

1. **DAVID TXT → Excel script**
   - Input: DAVID `gene2term` TXT file
   - Output: Excel file with columns = functional clusters, rows = locus tags

2. **Heatmap script**
   - Input: Excel file with:
     - First column: ordered locus tags (defines genome axis)
     - Other columns: gene clusters (from step 1)
   - Output: Heatmap PNG with cluster densities and KS test annotations

---

## ▶️ Usage

### 1. Generate Gene Clusters from DAVID TXT
Run:
```bash
python DAVID_gene2term_to_clusters.py
```
- Select DAVID TXT file via file picker.
- Excel file `<basename>_gene_clusters.xlsx` is created in the same folder.

### 2. Plot Gene Cluster Heatmap
Run:
```bash
python GeneClusterHeatmap_KS.py
```
- Select the Excel file (from step 1).
- Output: `gene_cluster_heatmap_KS.png` saved in the same folder.

---

## ⚙️ User Settings

**DAVID TXT → Excel script**
- Keyword groups defined in the `keyword_groups` dictionary at the top of the script.
- Add/modify groups freely.

**Heatmap script**
- `colormap` – matplotlib colormap (`plasma`, `viridis`, etc.)
- `sigma` – Gaussian kernel width (default 20)
- `spread_factor` – scales kernel width
- `height_per_cluster` – vertical spacing of rows
- `label_fontsize` – cluster label size
- `dpi` – output image resolution

---

## 📂 Example
- Start with a DAVID TXT file (gene2term output).
- Run clustering script → Excel with grouped clusters.
- Run heatmap script → density plot showing cluster enrichment along genome.

---

## 📖 Citation
If you use these tools in your research, please cite:
- The associated publication (once available).
- This repository via its Zenodo DOI: **[https://doi.org/10.5281/zenodo.17047999]**

---

## 📜 License
This project is released under the [MIT License](LICENSE).
