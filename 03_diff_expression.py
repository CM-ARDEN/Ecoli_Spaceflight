import os
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

def run_differential_expression():
    print("Diferansiyel Gen Ekspresyonu (DEG) Analizi Baslatiliyor...")
    
    input_path = "data/normalized_counts.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Gerekli dosya bulunamadi: {input_path}")
        
    df = pd.read_csv(input_path, index_col=0)
    
    # Ornek gruplarini ayirma
    flight_cols = [c for c in df.columns if "Flight" in c]
    ground_cols = [c for c in df.columns if "Ground" in c]
    
    # Ortalama ve Log2 Fold Change hesabi
    mean_flight = df[flight_cols].mean(axis=1)
    mean_ground = df[ground_cols].mean(axis=1)
    
    log2fc = np.log2((mean_flight + 1) / (mean_ground + 1))
    
    # Welch's t-test p-value hesabi
    p_values = []
    for gene in df.index:
        stat, p = stats.ttest_ind(df.loc[gene, flight_cols], df.loc[gene, ground_cols], equal_var=False)
        p_values.append(p if not np.isnan(p) else 1.0)
        
    # FDR (Benjamini-Hochberg) Duzeltmesi (padj hesabi)
    _, padj_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
    
    results = pd.DataFrame({
        'baseMean': (mean_flight + mean_ground) / 2,
        'log2FoldChange': log2fc,
        'pvalue': p_values,
        'padj': padj_values
    }, index=df.index)
    
    # Anlamli genlerin belirlenmesi (padj < 0.05 ve |log2FC| > 1)
    results['significant'] = (results['padj'] < 0.05) & (results['log2FoldChange'].abs() > 1.0)
    
    os.makedirs("data", exist_ok=True)
    results.to_csv("data/deg_results.csv")
    print(f"Analiz tamamlandi! Toplam {results['significant'].sum()} adet anlamli gen tespit edildi (FDR padj < 0.05).")

if __name__ == "__main__":
    run_differential_expression()