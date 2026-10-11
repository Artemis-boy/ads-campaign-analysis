"""Hitung CTR, CPC, conversion rate, CPA, ROAS per campaign & platform."""
import pandas as pd

REVENUE_PER_CONV = 150_000

df = pd.read_csv("data/clean/campaign_clean.csv")

def metrics(g):
    imp, klik, biaya, conv = g["impresi"].sum(), g["klik"].sum(), g["biaya"].sum(), g["konversi"].sum()
    return pd.Series({
        "impresi": imp, "klik": klik, "biaya": biaya, "konversi": conv,
        "CTR_%": round(klik / imp * 100, 2) if imp else 0,
        "CPC_Rp": round(biaya / klik, 0) if klik else 0,
        "conv_rate_%": round(conv / klik * 100, 2) if klik else 0,
        "CPA_Rp": round(biaya / conv, 0) if conv else 0,
        "ROAS": round(conv * REVENUE_PER_CONV / biaya, 2) if biaya else 0,
    })

by_campaign = df.groupby(["nama_campaign", "platform"]).apply(metrics, include_groups=False).reset_index()
by_campaign = by_campaign.sort_values("ROAS", ascending=False)
by_platform = df.groupby("platform").apply(metrics, include_groups=False).reset_index()

print("=== Per Campaign (sort ROAS) ===")
print(by_campaign.to_string(index=False))
print("\n=== Per Platform ===")
print(by_platform.to_string(index=False))

by_campaign.to_csv("output/summary_by_campaign.csv", index=False)
by_platform.to_csv("output/summary_by_platform.csv", index=False)
print("\nSaved -> output/summary_by_campaign.csv, output/summary_by_platform.csv")
