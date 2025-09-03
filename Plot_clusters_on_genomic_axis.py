"""
TITLE: Gene Cluster Heatmap with KS Significance

DESCRIPTION:
This script visualizes gene clusters along a genome axis using smoothed density heatmaps.
It uses a Gaussian kernel for each gene and applies a Kolmogorov-Smirnov test to assess 
whether gene positions in each cluster deviate significantly from a uniform distribution.

INPUT:
- Excel file with:
    • First column: ordered list of locus tags (defines genome axis)
    • Other columns: each column is a gene cluster (locus tags in that cluster)

OUTPUT:
- A heatmap figure as PNG with:
    • Cluster rows colored by gene density
    • Annotations for gene count and KS significance (n=xx, ***, etc)

USER SETTINGS:
- colormap: heatmap color scheme (e.g., 'viridis', 'plasma', 'YlGnBu')
- sigma: base Gaussian smoothing width (in genome positions)
- spread_factor: width multiplier to make bars thicker
- height_per_cluster: vertical height in inches per cluster
- label_fontsize: font size for row labels
- dpi: resolution of output PNG
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from scipy.stats import ks_1samp, uniform
import os

# === USER SETTINGS ===
colormap = 'plasma'
sigma = 20
spread_factor = 4
height_per_cluster = 0.3
label_fontsize = 10
dpi = 300

# === FUNCTIONS ===

def get_significance_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'ns'

def plot_gene_density_heatmap(reference_order, clusters_dict, sigma, spread_factor, cmap, height_scale, label_fontsize, output_file):
    reference_index = {locus: i for i, locus in enumerate(reference_order)}
    genome_length = len(reference_order)
    cluster_names = list(clusters_dict.keys())

    density_matrix = np.zeros((len(cluster_names), genome_length))
    cluster_labels = []

    for i, cluster_name in enumerate(cluster_names):
        loci = clusters_dict[cluster_name]
        indices = [reference_index[l] for l in loci if l in reference_index]

        density = np.zeros(genome_length)
        for idx in indices:
            adjusted_sigma = sigma * spread_factor
            window = np.arange(genome_length)
            gaussian = np.exp(-0.5 * ((window - idx) / adjusted_sigma) ** 2)
            density += gaussian

        density_matrix[i, :] = density / (np.max(density) + 1e-8)  # Normalize

        # KS test vs uniform distribution
        norm_positions = np.array(indices) / genome_length
        ks_stat, p_value = ks_1samp(norm_positions, uniform.cdf)

        label = f"{cluster_name} (n={len(indices)}, {get_significance_stars(p_value)})"
        cluster_labels.append(label)

    # === Plot ===
    fig_height = height_scale * len(cluster_names) + 1.5
    plt.figure(figsize=(14, fig_height))
    plt.imshow(density_matrix, aspect='auto', cmap=cmap, interpolation='nearest')
    plt.colorbar(label='Relative Gene Density')
    plt.yticks(np.arange(len(cluster_labels)), cluster_labels, fontsize=label_fontsize)
    plt.xticks([], [])
    plt.xlabel("Genome Position (Ordered Locus Tags)")
    plt.title("Gene Cluster Localization Heatmap (with KS Test)")
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi)
    plt.show()

# === MAIN ===

def main():
    print("=== Gene Cluster Heatmap with KS Test ===")
    print("Select Excel file with genome-ordered locus tags and gene clusters.")

    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not file_path:
        print("No file selected. Exiting.")
        return

    df = pd.read_excel(file_path)
    reference_order = df.iloc[:, 0].dropna().tolist()
    clusters = {col: df[col].dropna().tolist() for col in df.columns[1:]}

    output_path = os.path.join(os.path.dirname(file_path), "gene_cluster_heatmap_KS.png")
    print("Generating heatmap...")
    plot_gene_density_heatmap(reference_order, clusters, sigma, spread_factor,
                              colormap, height_per_cluster, label_fontsize, output_path)
    print(f"✅ Heatmap saved to:\n→ {output_path}")

if __name__ == "__main__":
    main()
