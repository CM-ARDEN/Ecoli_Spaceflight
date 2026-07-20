import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("📊 Volcano Plot Grafiği Oluşturuluyor...")

# 1. Analiz sonuçlarını yükle
df = pd.read_csv("data/ecoli_deg_results.csv")

# 2. P-value değerlerini görselleştirme için -log10'a çevir
# (0 olan p-value'ları çok küçük bir sayıyla değiştirerek hata almayı önle)
df['log10_p'] = -np.log10(df['p_value'].replace(0, 1e-10))

# 3. Grafik Alanını Oluştur
plt.figure(figsize=(10, 7))

# 4. Tüm genleri gri nokta olarak çiz
plt.scatter(df['log2FC'], df['log10_p'], c='grey', alpha=0.5, label='Fark Etmeyenler')

# 5. Anlamlı Genleri Renklendir (Kriter: |log2FC| > 0.5 ve p < 0.05)
up = df[(df['log2FC'] > 0.5) & (df['p_value'] < 0.05)]
down = df[(df['log2FC'] < -0.5) & (df['p_value'] < 0.05)]

plt.scatter(up['log2FC'], up['log10_p'], c='red', alpha=0.8, label=f'Artanlar ({len(up)})')
plt.scatter(down['log2FC'], down['log10_p'], c='blue', alpha=0.8, label=f'Azalanlar ({len(down)})')

# 6. Eşik Çizgilerini Ekle
plt.axhline(-np.log10(0.05), color='black', linestyle='--') # p=0.05 çizgisi
plt.axvline(0.5, color='black', linestyle='--')  # Artış çizgisi
plt.axvline(-0.5, color='black', linestyle='--') # Azalış çizgisi

# 7. Etiketler ve Başlık
plt.title("E. coli Uzay Stresi Volcano Plot (Flight vs GC)", fontsize=15)
plt.xlabel("Log2 Fold Change (Değişim Miktarı)", fontsize=12)
plt.ylabel("-Log10 P-value (İstatistiksel Anlamlılık)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# 8. Grafiği Kaydet ve Göster
plt.savefig("data/volcano_plot.png", dpi=300)
print("\n🎉 Volcano plot 'data/volcano_plot.png' olarak kaydedildi!")
print("👀 Grafiği açmak için terminale 'start data/volcano_plot.png' yazabilirsin.")

# Bazı sistemlerde grafiği pencerede açar:
plt.show()