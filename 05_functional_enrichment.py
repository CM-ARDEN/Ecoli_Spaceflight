import os
import pandas as pd
import matplotlib.pyplot as plt
import gseapy as gp


def run_functional_enrichment():
    print("Fonksiyonel Zenginlestirme Analizi Baslatiliyor...")

    input_path = os.path.join("data", "deg_results.csv")
    output_dir = os.path.join("data", "enrichment_results")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_path):
        print(f"Hata: {input_path} bulunamadi. Lutfen once 03_diff_expression.py calistirin.")
        return

    # deg_results.csv index sütunu gen isimleridir
    df = pd.read_csv(input_path, index_col=0)

    # Anlamli genleri filtrele (padj < 0.05 ve |log2FoldChange| > 1.0)
    sig_genes_df = df[(df['padj'] < 0.05) & (df['log2FoldChange'].abs() > 1.0)]
    gene_list = sig_genes_df.index.astype(str).tolist()

    print(f"Zenginlestirme analizi icin {len(gene_list)} adet istatistiksel olarak anlamli gen bulundu.")

    if len(gene_list) == 0:
        print("Uyari: Esikleri gecen anlamli gen bulunamadigi icin zenginlestirme yapilamadi.")
        return

    # E. coli Gen Zenginlestirmesi
    # Not: E. coli icin gene_sets parametresinde bakteriyel ontoloji veya g:Profiler tercih edilir.
    try:
        # GSEApy Enrichr sorgusu
        enr = gp.enrichr(
            gene_list=gene_list,
            gene_sets=['GO_Biological_Process_2023'],
            outdir=output_dir,
            cutoff=0.05
        )

        if not enr.results.empty:
            plot_path = os.path.join("data", "enrichment_plot.png")
            gp.barplot(
                enr.res2d,
                column="Adjusted P-value",
                group='Gene_set',
                size=10,
                top_term=10,
                ofname=plot_path
            )
            print(f"Fonksiyonel analiz basariyla tamamlandi: {plot_path}")
        else:
            print("Belirtilen esiklerde anlamli zenginlestirilmis yolak bulunamadi.")

    except Exception as e:
        print(f"Enrichment servisi calisirken bir hata olustu: {e}")


if __name__ == "__main__":
    run_functional_enrichment()
