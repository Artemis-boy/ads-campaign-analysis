"""Generate dummy Meta Ads-style campaign data (dirty, ~3000 rows)."""
import random
from datetime import date, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

CAMPAIGNS = [
    ("Promo Lebaran Sale", "FB"),
    ("Brand Awareness Q1", "FB"),
    ("Retargeting Pengunjung", "FB"),
    ("Launch Produk Baru", "IG"),
    ("Flash Sale Weekend", "IG"),
    ("Katalog K fashion", "IG"),
    ("Video Engagement", "FB"),
]

START = date(2026, 4, 11)
END = date(2026, 10, 10)
days = (END - START).days

N = 3000
rows = []
for _ in range(N):
    d = START + timedelta(days=random.randint(0, days))
    # random date format: YYYY-MM-DD vs DD/MM/YYYY
    if random.random() < 0.35:
        tanggal = d.strftime("%d/%m/%Y")
    else:
        tanggal = d.strftime("%Y-%m-%d")
    nama, platform = random.choice(CAMPAIGNS)
    impresi = int(np.random.randint(800, 15000))
    ctr_base = random.uniform(0.008, 0.035)
    klik = max(1, int(impresi * ctr_base * random.uniform(0.7, 1.3)))
    cpc = random.uniform(800, 4500)
    biaya = round(klik * cpc, 0)
    conv_rate = random.uniform(0.02, 0.12)
    konversi = max(0, int(klik * conv_rate * random.uniform(0.6, 1.4)))
    rows.append([tanggal, nama, platform, impresi, klik, biaya, konversi])

df = pd.DataFrame(rows, columns=["tanggal", "nama_campaign", "platform", "impresi", "klik", "biaya", "konversi"])

# Sengaja kotor:
# 1. duplikat ~3%
dup = df.sample(frac=0.03, random_state=1)
df = pd.concat([df, dup], ignore_index=True)

# 2. sel kosong ~2% per kolom numerik
for col in ["impresi", "klik", "biaya", "konversi"]:
    idx = df.sample(frac=0.02, random_state=hash(col) % 100).index
    df.loc[idx, col] = np.nan

# 3. outlier biaya 2 baris
df.loc[df.index[:2], "biaya"] = [95_000_000, 120_000_000]

df.to_csv("data/raw/campaign_data.csv", index=False)
print(f"Saved {len(df)} rows -> data/raw/campaign_data.csv")
print(df.head(3).to_string())
