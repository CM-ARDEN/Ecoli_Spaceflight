import os
import pandas as pd
import gseapy as gp
import matplotlib.pyplot as plt

def run_functional_enrichment():
    input_path = os.path.join("data", "deg_results.csv")
    output_dir = os.path.join("data", "enrichment_results")
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"Hata: {input_path} bulunamadı. Lütfen önce 03_diff_expression.py çalıştırın.")
        return

    df = pd.read_csv(input_path)
    
    # Anlamlı genleri filtrele (padj < 0.05 ve |log2FC| > 1.0)
    sig_genes_df = df[(df['padj'] < 0.05) & (df['log2FC'].abs() > 1.0)]
    gene_list = sig_genes_df['Gene'].dropna().astype(str).tolist()
    
    print(f"Zenginleştirme analizi için {len(gene_list)} adet istatistiksel olarak anlamlı gen bulundu.")
    
    if len(gene_list) == 0:
        print("Uyarı: Eşikleri geçen anlamlı gen bulunamadığı için zenginleştirme yapılamadı.")
        return

    # Gene Ontology (Biological Process) ve KEGG Zenginleştirmesi
    try:
        enr = gp.enrichr(
            gene_list=gene_list,
            gene_sets=['GO_Biological_Process_2023', 'KEGG_2021_Human'],
            outdir=output_dir,
            cutoff=0.05
        )
        
        # İlk 10 terimi barplot olarak kaydet
        plot_path = os.path.join("data", "enrichment_plot.png")
        gp.barplot(
            enr.res2d,
            column="Adjusted P-value",
            group='Gene_set',
            size=10,
            top_term=10,
            ofname=plot_path
        )
        print(f"Fonksiyonel analiz başarıyla tamamlandı: {plot_path}")
    except Exception as e:
        print(f"Enrichment servisi çalışırken bir hata oluştu: {e}")

if __name__ == "__main__":
    run_functional_enrichment()
