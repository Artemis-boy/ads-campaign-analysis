"""Clean raw campaign data -> data/clean/campaign_clean.csv with log."""
import pandas as pd
import numpy as np

RAW = "data/raw/campaign_data.csv"
OUT = "data/clean/campaign_clean.csv"

df = pd.read_csv(RAW)
n0 = len(df)
print(f"[clean] raw rows: {n0}")

# 1. Drop exact duplicates
dup = df.duplicated().sum()
df = df.drop_duplicates()
print(f"[clean] duplicates removed: {dup}")

# 2. Parse mixed date formats (YYYY-MM-DD & DD/MM/YYYY)
def parse_mixed(s):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return pd.to_datetime(s, format=fmt)
        except Exception:
            continue
    return pd.NaT

df["tanggal"] = df["tanggal"].apply(parse_mixed)
bad_date = df["tanggal"].isna().sum()
df = df.dropna(subset=["tanggal"])
print(f"[clean] bad dates removed: {bad_date}")

# 3. Drop rows with empty numeric cells
na_rows = df[["impresi", "klik", "biaya", "konversi"]].isna().any(axis=1).sum()
df = df.dropna(subset=["impresi", "klik", "biaya", "konversi"])
print(f"[clean] rows with empty cells removed: {na_rows}")

# 4. Remove cost outliers via IQR
q1, q3 = df["biaya"].quantile(0.25), df["biaya"].quantile(0.75)
iqr = q3 - q1
cap = q3 + 1.5 * iqr
out = (df["biaya"] > cap).sum()
df = df[df["biaya"] <= cap]
print(f"[clean] cost outliers removed (cap Rp{cap:,.0f}): {out}")

# 5. Cast types + sort
for c in ["impresi", "klik", "biaya", "konversi"]:
    df[c] = df[c].astype(int)
df = df.sort_values("tanggal").reset_index(drop=True)

df.to_csv(OUT, index=False)
print(f"[clean] final rows: {len(df)} (removed {n0 - len(df)}) -> {OUT}")
