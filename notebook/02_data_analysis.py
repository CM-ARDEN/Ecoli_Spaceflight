import pandas as pd

print("📊 E. coli Gen Analizi Başlatılıyor...")

# 1. Oluşturduğumuz veri matrisini yüklüyoruz
df = pd.read_csv("data/ecoli_counts.csv")

print("\n✅ Matris Başarıyla Yüklendi. İlk 5 Satır:")
print(df.head())

# 2. Örnek bazlı toplam okuma sayıları
sample_cols = [c for c in df.columns if c != 'gene_id']
print("\n📈 Örnek Başına Toplam Read Sayıları:")
print(df[sample_cols].sum())

# 3. CPM (Counts Per Million) Normalizasyonu
cpm_df = df.copy()
for col in sample_cols:
    cpm_df[col] = (df[col] / df[col].sum()) * 1e6

print("\n✨ CPM ile Normalize Edilmiş Veri (İlk 5 Satır):")
print(cpm_df.head())

# Kaydet
cpm_df.to_csv("data/ecoli_cpm_normalized.csv", index=False)
print("\n🎉 Normalize edilmiş veri 'data/ecoli_cpm_normalized.csv' olarak kaydedildi!")