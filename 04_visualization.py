import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_volcano_plot():
    print("Volcano Plot Gorsellestirmesi Hazirlaniyor...")
    
    deg_path = "data/deg_results.csv"
    if not os.path.exists(deg_path):
        raise FileNotFoundError(f"Gerekli DEG sonuclari bulunamadi: {deg_path}")
        
    df = pd.read_csv(deg_path, index_col=0)
    
    # -log10(padj) hesabi (0 degeri icin koruma eklendi)
    df['minus_log10_padj'] = -np.log10(df['padj'].replace(0, 1e-300))
    
    plt.figure(figsize=(10, 7))
    
    # Anlamlilik durumlari
    up_regulated = df[(df['padj'] < 0.05) & (df['log2FoldChange'] > 1.0)]
    down_regulated = df[(df['padj'] < 0.05) & (df['log2FoldChange'] < -1.0)]
    not_sig = df[(df['padj'] >= 0.05) | (df['log2FoldChange'].abs() <= 1.0)]
    
    plt.scatter(not_sig['log2FoldChange'], not_sig['minus_log10_padj'], color='grey', alpha=0.4, label='Not Significant', s=15)
    plt.scatter(up_regulated['log2FoldChange'], up_regulated['minus_log10_padj'], color='#d95f02', alpha=0.8, label=f'Up-regulated (padj<0.05, FC>1) [{len(up_regulated)}]', s=25)
    plt.scatter(down_regulated['log2FoldChange'], down_regulated['minus_log10_padj'], color='#7570b3', alpha=0.8, label=f'Down-regulated (padj<0.05, FC<-1) [{len(down_regulated)}]', s=25)
    
    # Esik cizgileri
    plt.axhline(-np.log10(0.05), color='black', linestyle='--', linewidth=0.8, label='FDR padj = 0.05')
    plt.axvline(1.0, color='blue', linestyle=':', linewidth=0.8)
    plt.axvline(-1.0, color='blue', linestyle=':', linewidth=0.8)
    
    plt.title('E. coli Spaceflight vs Ground DEG Volcano Plot', fontsize=14, fontweight='bold')
    plt.xlabel('log2(Fold Change)', fontsize=12)
    plt.ylabel('-log10(padj)', fontsize=12)
    plt.legend(loc='upper right', frameon=True)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    os.makedirs("data", exist_ok=True)
    out_img = "data/volcano_plot.png"
    plt.savefig(out_img, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Volcano Plot basariyla kaydedildi: {out_img}")

if __name__ == "__main__":
    generate_volcano_plot()