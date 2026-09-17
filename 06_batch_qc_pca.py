import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def run_pca_and_batch_qc():
    input_path = os.path.join("data", "normalized_cpm.csv")
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"Hata: {input_path} bulunamadı. Lütfen önce 02_data_analysis.py çalıştırın.")
        return

    # CPM verisini oku (Satırlar: Genler, Sütunlar: Örnekler)
    df = pd.read_csv(input_path, index_col=0)
    
    # Sayısal değerleri log2(CPM + 1) dönüşümüne sok
    log_cpm = np.log2(df + 1).T  # Transpoz alarak Satırlar: Örnekler, Sütunlar: Genler yapıyoruz
    
    # PCA Hesapla (İlk 2 bileşen)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(log_cpm)
    
    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'], index=log_cpm.index)
    
    # Örnek gruplarını ayıkla (Flight vs Ground)
    pca_df['Condition'] = ['Flight' if 'flight' in s.lower() else 'Ground' for s in pca_df.index]
    
    # Görselleştirme
    plt.figure(figsize=(8, 6))
    for condition, color in [('Flight', '#dc2626'), ('Ground', '#2563eb')]:
        subset = pca_df[pca_df['Condition'] == condition]
        plt.scatter(subset['PC1'], subset['PC2'], label=condition, color=color, s=120, edgecolors='black', alpha=0.8)
    
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% Açıklanan Varyans)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% Açıklanan Varyans)")
    plt.title("Sample Level PCA & Batch Effect Assessment")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Biological Condition")
    plt.tight_layout()
    
    out_plot = os.path.join(output_dir, "pca_batch_qc.png")
    plt.savefig(out_plot, dpi=300)
    plt.close()
    print(f"PCA & Batch QC analizi tamamlandı: {out_plot}")

if __name__ == "__main__":
    run_pca_and_batch_qc()
