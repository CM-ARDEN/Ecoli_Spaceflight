import pandas as pd
import numpy as np
from scipy import stats

print("🧬 Farklı İfade Edilen Gen Analizi (DEG) Başlatılıyor...")

# Normalize veriyi yükle
df = pd.read_csv("data/ecoli_cpm_normalized.csv")

flight_cols = ['Flight_Rep1', 'Flight_Rep2', 'Flight_Rep3']
gc_cols = ['GC_Rep1', 'GC_Rep2', 'GC_Rep3']

# Ortalama ifade değerleri ve Log2 Fold Change (L2FC) hesabı
df['Flight_Mean'] = df[flight_cols].mean(axis=1)
df['GC_Mean'] = df[gc_cols].mean(axis=1)

# Log2 Fold Change: log2(Flight / GC)
df['log2FC'] = np.log2((df['Flight_Mean'] + 1) / (df['GC_Mean'] + 1))

# Welch t-testi ile p-value hesabı
p_values = []
for idx, row in df.iterrows():
    f_vals = row[flight_cols].values.astype(float)
    g_vals = row[gc_cols].values.astype(float)
    _, pval = stats.ttest_ind(f_vals, g_vals, equal_var=False)
    p_values.append(pval)

df['p_value'] = p_values

# Anlamlı genleri belirle (|log2FC| > 0.5 ve p_value < 0.05)
up_regulated = df[(df['log2FC'] > 0.5) & (df['p_value'] < 0.05)]
down_regulated = df[(df['log2FC'] < -0.5) & (df['p_value'] < 0.05)]

print(f"\n🚀 Uzay koşullarında ifadesi ARTAN gen sayısı: {len(up_regulated)}")
print(f"📉 Uzay koşullarında ifadesi AZALAN gen sayısı: {len(down_regulated)}")

# Sonuçları kaydet
df.to_csv("data/ecoli_deg_results.csv", index=False)
print("\n🎉 Tüm DEG sonuçları 'data/ecoli_deg_results.csv' dosyasına kaydedildi!")