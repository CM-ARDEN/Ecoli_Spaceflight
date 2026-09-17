# Q1 Internal Review Revision Notes

**Project:** Ecoli Spaceflight: Reproducible Transcriptomic Analysis of *Escherichia coli* Responses to Spaceflight  
**Lead Researcher:** Arden Avidoğlu  
**Evaluation Scope:** Q1 Internal Review Addressed Improvements  

---

### Summary of Revisions Addressed

| Priority | Feedback Point | Pipeline Implementation / Resolution |
| :--- | :--- | :--- |
| **Very High** | Primary Biological Hypothesis | Explicit hypothesis defined covering membrane permeability, molecular chaperones, and RpoS stress regulation under low shear stress. |
| **Very High** | QC Criteria Reporting | Detailed in `README.md` covering FastQC metrics (Phred >= 30), unique alignment thresholds (>= 85%), and low-count CPM filtering. |
| **Very High** | Statistical Method & FDR Strategy | Documented Welch's t-test (`equal_var=False`) and Benjamini-Hochberg FDR (`padj < 0.05`, `|log2FC| > 1.0`). |
| **High** | Functional Enrichment (GO & KEGG) | Implemented automated `05_functional_enrichment.py` evaluating biological processes and KEGG pathways. |
| **High** | Batch Effect Evaluation | Implemented `06_batch_qc_pca.py` providing sample-level Principal Component Analysis to verify biological separation over technical batch noise. |

---

### Architectural Additions

- `05_functional_enrichment.py`: Generates Gene Ontology (Biological Process) and KEGG enrichment barplots.
- `06_batch_qc_pca.py`: Computes 2D PCA ordinations from log2(CPM + 1) matrices.
- `requirements.txt`: Updated with `gseapy` and `scikit-learn` dependencies.
