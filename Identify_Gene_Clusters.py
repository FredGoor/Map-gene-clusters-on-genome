# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 13:29:04 2025

@author: Frederic
"""

# DAVID annotation TXT to Excel converter – Multi-keyword group clustering
# Description:
# This script loads a DAVID gene2term TXT file, matches user-defined keyword groups to all annotation columns,
# and outputs an Excel file where each column contains locus tags matching one keyword group (i.e. gene cluster).

import pandas as pd
from tkinter import Tk, filedialog
import os

# === USER SETTINGS ===
# Each line below defines a keyword group. Each group will become one column in the output Excel file.
# You can modify or add groups freely.
keyword_groups = {
    "Secretion": ["secretion", "secreted", "type iii", "type iv"],
    "DNA mobility": ["transposition", "transposase", "integrase", "recombinase", "recombination"],
    "quorum sensing": ["quorum sensing"],
    "Virulence": ["virulence", "pathogenesis", "toxin", "effector", "host", "infection", "invasion"],
    "virulence+secretion": ["secretion", "secreted", "type iii", "type iv", "virulence", "pathogenesis", "toxin", "effector", "host", "infection", "invasion"],
    "LPS": ["LPS", "lipopolysaccharide", "o antigen", "o-antigen", "lipid a", "core oligosaccharide", "lps biosynthesis", "lipopolysaccharide biosynthetic process", "waa", "wba"],
    "Motility": ["flagellum", "flagellar", "motility", "chemotaxis"],
    "Phages": ["phage", "phages", "prophage", "prophages"],
    "Translation": ["translation", "ribosome", "rRNA", "ribosomal", "ribonucleoprotein", "EFTU"],
    "Cell Division": ["cell division", "cytokinesis", "septum", "fission", "binary fission", "divisome", "FtsZ", "FtsA", "FtsI", "FtsQ", "FtsK", "FtsL", "FtsN", "FtsW", "FtsB", "MinC", "MinD", "MinE", "Z-ring", "midcell", "division site"],
    "Amino acid biosynthesis": ["amino acid biosynthesis", "amino-acid biosynthesis", "amino acid synthesis", "amino-acid synthesis"],
    "Glycolysis": ["glycolysis"],
    "Carbon metabolism": ["ubiquinone", "TCA", "carbon metabolism", "tricarboxylic acid", "citrate cycle"],
    "Cytochrome": ["cytochrome"],
    "4Fe-4S": ["sulfur cluster", "4Fe-4S"],
    "Transmembrane": ["Siderophore", "ABC", "transporter", "permease", "porin", "heme", "electron transport", "transmembrane"],
    "Adhesion": ["adhesion", "fimbriae", "pili", "flagellum", "LPS", "lipopolysaccharide"],
    "Anaeroby": ["anaeroby", "anaerobic", "fumarate reductase", "nitrate reductase", "anaerobic respiration", "nitrite", "formate dehydrogenase", "pyruvate formate-lyase", "anaerobic growth"],
    "Acid stress": ["acid stress", "acid resistance", "low pH", "acid tolerance", "proton motive force", "glutamate decarboxylase", "gadA", "gadB", "gadC", "acid shock"],
    "Heat shock": ["heat shock", "chaperone", "dnaK", "groEL", "groES", "grpE", "hsp", "heat inducible", "temperature stress", "thermotolerance"],
    "SOS response": ["SOS response", "dna damage", "recA", "lexA", "umuC", "umuD", "dinB", "error-prone repair", "nucleotide excision repair", "uv damage"],
    "Oxidative stress": ["oxidative stress", "superoxide", "catalase", "sodA", "sodB", "peroxidase", "hydrogen peroxide", "ROS", "oxyR", "soxR", "soxS"],
    "Envelope stress": ["envelope stress", "cpx", "bacterial envelope", "degP", "surA", "sigmaE", "omp", "misfolded protein", "outer membrane protein"],
    "Osmotic stress": ["osmotic stress", "osmoregulation", "osmoprotectant", "proP", "betT", "kdp", "osmY", "high salt", "NaCl"],
    "Cold shock": ["cold shock", "cspA", "cspB", "low temperature", "cold inducible", "RNA chaperone"],
    "Nutrient limitation": ["nutrient limitation", "nutrient starvation", "starvation response", "carbon starvation", "phosphate starvation", "phoB", "phoR", "cAMP", "crp", "nutrient stress"],
    "tRNA charging":["tRNAs","tRNA","aminoacyl-tRNA synthetase", "tRNA charging", "tRNA ligase", "tRNA synthetase", "aminoacylation"],
    "TCA cycle": ["TCA cycle", "tricarboxylic acid cycle", "citrate cycle", "citrate synthase", "aconitase", "isocitrate dehydrogenase", "α-ketoglutarate dehydrogenase", "succinyl-CoA synthetase", "succinate dehydrogenase", "fumarase", "malate dehydrogenase", "oxidative decarboxylation"]
}



# === FILE PICKER: Load DAVID annotation TXT file ===
Tk().withdraw()
input_txt = filedialog.askopenfilename(title="Select DAVID gene2term TXT File", filetypes=[("Text Files", "*.txt")])
if not input_txt:
    raise Exception("No file selected.")

# === Prepare output Excel file path ===
base = os.path.splitext(os.path.basename(input_txt))[0]
output_excel = os.path.join(os.path.dirname(input_txt), base + "_gene_clusters.xlsx")

# === Load DAVID annotation table ===
df = pd.read_csv(input_txt, sep='\t', dtype=str)

# === Clean: strip trailing commas in all cells ===
for col in df.columns:
    df[col] = df[col].str.rstrip(',')

# === Build cluster results ===
cluster_dict = {}

for group_name, keywords in keyword_groups.items():
    matched_genes = set()
    for _, row in df.iterrows():
        row_text = ' '.join(row.astype(str).values).lower()
        if any(kw in row_text for kw in keywords):
            matched_genes.add(row.iloc[0])  # Assume locus tag is in first column
    cluster_dict[group_name] = sorted(matched_genes)

# === Build DataFrame: one column per group ===
max_len = max(len(genes) for genes in cluster_dict.values())
cluster_df = pd.DataFrame({group: pd.Series(genes) for group, genes in cluster_dict.items()})

# === Export to Excel ===
cluster_df.to_excel(output_excel, index=False)
print(f"✅ Gene clusters exported to: {output_excel}")
