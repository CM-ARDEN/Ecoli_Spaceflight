# E. coli Spaceflight Gene Expression & DEG Pipeline

A reproducible bioinformatics workflow analyzing *Escherichia coli* transcriptomic responses to spaceflight microgravity using NASA GeneLab data (OSDR-728).

---

## Primary Research Hypothesis

Spaceflight microgravity and low-shear fluid dynamics disrupt bacterial membrane equilibrium in *Escherichia coli*, inducing significant transcriptional up-regulation of outer membrane porins, molecular chaperones, and RpoS-dependent general stress adaptation pathways compared to 1g ground controls, accompanied by a targeted down-regulation of non-essential ribosomal biosynthesis to preserve cellular energetics.

---

## Quality Control & Statistical Framework

| Parameter / Stage | Criteria & Pipeline Implementation | Methodological Rationale |
| :--- | :--- | :--- |
| **Raw Read Quality Control** | FastQC & MultiQC (Phred score >= 30) | Elimination of low-quality base calls and sequencing artifacts |
| **Genome Alignment** | Reference Genome: *E. coli* K-12 (>= 85% unique alignment) | High-specificity alignment avoiding non-specific genomic mapping |
| **Low Count Filtering** | CPM >= 1.0 across biological replicates | Removal of stochastic transcriptional noise and unexpressed genes |
| **Batch Effect / Sample QC** | Principal Component Analysis (PCA) | Verification of biological separation without technical batch confounding |
| **Variance Heterogeneity** | Welch's t-test (`scipy.stats.ttest_ind`, `equal_var=False`) | Correction for unequal group variances inherent in spaceflight stress |
| **Multiple Testing Correction** | Benjamini-Hochberg FDR (`statsmodels.stats.multitest`) | Strict control of False Discovery Rate (Type I error) |
| **Significance Thresholds** | padj < 0.05 and |log2FC| > 1.0 | Ensuring both high statistical confidence and biological effect size |
| **Functional Enrichment** | Gene Ontology (Biological Process) & KEGG Pathways | Biological validation and systems-level pathway interpretation |

---

## Pipeline Architecture

- `01_data_download.py`: Automated retrieval of NASA GeneLab OSDR-728 unnormalized count matrices.
- `02_data_analysis.py`: Sample depth assessment, low-count filtering, and CPM normalization.
- `03_diff_expression.py`: Welch's t-test with Benjamini-Hochberg FDR correction.
- `04_visualization.py`: Volcano plot generation scaled by -log10(padj) vs. log2FC.
- `05_functional_enrichment.py`: Automated GO and KEGG pathway overrepresentation analysis.
- `06_batch_qc_pca.py`: Sample-level PCA ordination and batch effect assessment.

---

## Installation & Execution

```bash
pip install -r requirements.txt
python 01_data_download.py
python 02_data_analysis.py
python 03_diff_expression.py
python 04_visualization.py
python 05_functional_enrichment.py
python 06_batch_qc_pca.py
