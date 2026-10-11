"""Laporan PDF Bahasa Indonesia: 3+ temuan + 3 rekomendasi + grafik."""
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

camp = pd.read_csv("output/summary_by_campaign.csv")
plat = pd.read_csv("output/summary_by_platform.csv")

top = camp.iloc[0]
low = camp.iloc[-1]
ig = plat[plat.platform == "IG"].iloc[0]
fb = plat[plat.platform == "FB"].iloc[0]

pdf = FPDF()
pdf.set_margins(15, 15, 15)
pdf.set_auto_page_break(True, 20)
pdf.add_page()
W = pdf.epw
pdf.set_font("Helvetica", "B", 18)
pdf.multi_cell(w=W, h=9, text="Analisis Campaign Iklan (Meta Ads)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(w=W, h=6, text="Periode: April - Oktober 2026 | 7 campaign (FB & IG) | 2.634 baris bersih", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(4)

pdf.set_font("Helvetica", "B", 13)
pdf.multi_cell(w=W, h=8, text="1. Ringkasan Metrik", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "", 11)
pdf.set_x(15)
pdf.multi_cell(w=W, h=6, new_x=XPos.LMARGIN, new_y=YPos.NEXT, text=
    f"Total biaya Rp{camp.biaya.sum():,.0f} menghasilkan {camp.konversi.sum():,.0f} konversi. "
    f"ROAS rata-rata {(camp.konversi.sum()*150_000/camp.biaya.sum()):.2f}x "
    f"(asumsi Rp150.000/konversi). Platform IG unggul: ROAS {ig.ROAS}x vs FB {fb.ROAS}x, "
    f"CPA IG Rp{ig.CPA_Rp:,.0f} vs FB Rp{fb.CPA_Rp:,.0f}.")
pdf.ln(2)

pdf.set_font("Helvetica", "B", 13)
pdf.multi_cell(w=W, h=8, text="2. Temuan Utama", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "", 11)
temuan = [
    f"Retargeting Pengunjung (FB) paling efisien: ROAS {top.ROAS}x, CPA Rp{top.CPA_Rp:,.0f} terendah, "
    f"conversion rate 6,70%. Audiens hangat mengkonversi jauh lebih murah.",
    f"Flash Sale Weekend (IG) volume terbaik: {camp.konversi.max():,.0f} konversi dengan ROAS 4,13x. "
    f"Promo berbasis urgensi bekerja kuat di Instagram.",
    f"Promo Lebaran Sale (ROAS {low.ROAS}x, CPA Rp{low.CPA_Rp:,.0f}) dan Brand Awareness Q1 (ROAS 3,78x) "
    f"jadi dua campaign terboros. CTR semua campaign stagnan di 2,0-2,1% "
    f"sehingga pembeda profitabilitas ada di conversion rate dan CPA, bukan klik.",
    f"Instagram mengalahkan Facebook di ROAS ({ig.ROAS}x vs {fb.ROAS}x) dan conversion rate "
    f"({ig['conv_rate_%']}% vs {fb['conv_rate_%']}%), walau CTR nyaris sama. Budget di FB kurang produktif.",
]
for i, t in enumerate(temuan, 1):
    pdf.set_x(15)
    pdf.multi_cell(w=W, h=6, new_x=XPos.LMARGIN, new_y=YPos.NEXT, text=f"{i}. {t}")
pdf.ln(2)

pdf.set_font("Helvetica", "B", 13)
pdf.multi_cell(w=W, h=8, text="3. Rekomendasi Bisnis", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "", 11)
rekom = [
    "Realokasi 20-30% budget dari Promo Lebaran Sale & Brand Awareness Q1 ke Retargeting Pengunjung "
    "dan Flash Sale Weekend. Potensi kenaikan konversi ~10-15% tanpa menambah total budget.",
    "Scale up Instagram: naikkan porsi budget IG dari 45% ke ~60% bertahap per 2 minggu, "
    "pantau CPA tetap di bawah Rp38.000; jika jebol, rollback.",
    "Perbaiki funnel bawah untuk campaign boros: ganti landing page Promo Lebaran (target conv rate 6,5%), "
    "A/B test 3 varian kreatif baru karena CTR stagnan 2%, dan pasang frequency cap + CPA cap Rp38.000 "
    "agar outlier biaya tidak terulang.",
]
for i, r in enumerate(rekom, 1):
    pdf.set_x(15)
    pdf.multi_cell(w=W, h=6, new_x=XPos.LMARGIN, new_y=YPos.NEXT, text=f"{i}. {r}")
pdf.ln(2)

pdf.set_font("Helvetica", "B", 13)
pdf.multi_cell(w=W, h=8, text="4. Visualisasi", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
for img, w in [("output/roas_per_campaign.png", 165),
               ("output/tren_biaya_konversi.png", 165),
               ("output/ctr_per_platform.png", 110),
               ("output/scatter_cpc_convrate.png", 130)]:
    pdf.image(img, w=w)
    pdf.ln(3)

pdf.output("output/laporan_campaign.pdf")
print("Saved -> output/laporan_campaign.pdf")
