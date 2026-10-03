import pandas as pd

print("E. coli Gen Analizi ve Filtreleme Baslatiliyor...")

# 1. Ham sayim matrisini yukleme
df = pd.read_csv("data/ecoli_counts.csv")

print("\nMatris Basariyla Yuklendi. Ilk 5 Satir:")
print(df.head())

# 2. Ornek bazli toplam okuma sayilari
sample_cols = [c for c in df.columns if c != 'gene_id']
print("\nOrnek Basina Toplam Read Sayilari:")
print(df[sample_cols].sum())

# 3. CPM (Counts Per Million) Normalizasyonu
cpm_df = df.copy()
for col in sample_cols:
    cpm_df[col] = (df[col] / df[col].sum()) * 1e6

print("\nCPM ile Normalize Edilmis Veri (Ilk 5 Satir):")
print(cpm_df.head())

# 4. Dusuk Sayim Filtreleme (Low-Count Filtering)
# Biyolojik tekrarlar arasinda en az 2 ornekte CPM >= 1.0 kriteri
cpm_threshold = 1.0
min_samples = 2
keep = (cpm_df[sample_cols] >= cpm_threshold).sum(axis=1) >= min_samples

cpm_filtered_df = cpm_df[keep].reset_index(drop=True)

print(f"\nFiltreleme Sonuclari:")
print(f"Toplam Gen Sayisi: {len(cpm_df)}")
print(f"Filtreleme Sonrasi Kalan Gen Sayisi (CPM >= {cpm_threshold}): {len(cpm_filtered_df)}")

# 5. Filtrelenmis ve Normalize Edilmis Veriyi Kaydetme
cpm_filtered_df.to_csv("data/ecoli_cpm_normalized.csv", index=False)
print("\nNormalize ve filtre edilmis veri 'data/ecoli_cpm_normalized.csv' olarak kaydedildi.")
