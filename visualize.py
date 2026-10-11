"""4 grafik: tren bulanan, ROAS per campaign, CTR per platform, scatter CPC vs conv rate."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REVENUE = 150_000
df = pd.read_csv("data/clean/campaign_clean.csv", parse_dates=["tanggal"])
camp = pd.read_csv("output/summary_by_campaign.csv")
plat = pd.read_csv("output/summary_by_platform.csv")

plt.rcParams.update({"figure.dpi": 120, "font.size": 10})

# 1. Tren biaya vs konversi per bulan
m = df.copy()
m["bulan"] = m["tanggal"].dt.to_period("M").astype(str)
monthly = m.groupby("bulan").agg(biaya=("biaya", "sum"), konversi=("konversi", "sum")).reset_index()
fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.plot(monthly["bulan"], monthly["biaya"] / 1e6, marker="o", label="Biaya (Rp jt)")
ax1.set_ylabel("Biaya (Rp juta)")
ax2 = ax1.twinx()
ax2.bar(monthly["bulan"], monthly["konversi"], alpha=0.45, label="Konversi")
ax2.set_ylabel("Konversi")
ax1.set_title("Tren Biaya vs Konversi per Bulan")
plt.xticks(rotation=30)
fig.tight_layout()
fig.savefig("output/tren_biaya_konversi.png")
plt.close(fig)

# 2. ROAS per campaign
c2 = camp.sort_values("ROAS")
plt.figure(figsize=(9, 4.5))
plt.barh(c2["nama_campaign"], c2["ROAS"])
plt.xlabel("ROAS (x)")
plt.title("ROAS per Campaign (1 konversi = Rp150rb)")
plt.tight_layout()
plt.savefig("output/roas_per_campaign.png")
plt.close()

# 3. CTR per platform
plt.figure(figsize=(6, 4))
plt.bar(plat["platform"], plat["CTR_%"])
plt.ylabel("CTR (%)")
plt.title("CTR per Platform")
plt.tight_layout()
plt.savefig("output/ctr_per_platform.png")
plt.close()

# 4. Scatter CPC vs conversion rate per campaign
plt.figure(figsize=(7, 5))
plt.scatter(camp["CPC_Rp"], camp["conv_rate_%"])
for _, r in camp.iterrows():
    plt.annotate(r["nama_campaign"].split()[0], (r["CPC_Rp"], r["conv_rate_%"]), fontsize=8)
plt.xlabel("CPC (Rp)")
plt.ylabel("Conversion rate (%)")
plt.title("CPC vs Conversion Rate per Campaign")
plt.tight_layout()
plt.savefig("output/scatter_cpc_convrate.png")
plt.close()

print("Saved 4 PNG -> output/")
