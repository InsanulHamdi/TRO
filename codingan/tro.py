import pulp
import numpy as np

# 1. Definisikan Data Model

# Gudang (Sumber/Supply) dan Kapasitas (Supply)
gudang = ["Kudus", "Surabaya", "Malang", "Blitar", "Kediri"]
kapasitas = {"Kudus": 120, "Surabaya": 140, "Malang": 100, "Blitar": 150, "Kediri": 130}

# Toko (Tujuan/Demand) dan Permintaan (Demand)
toko = ["Semarang", "Yogyakarta", "Solo", "Tuban", "Madiun", "Banyuwangi"]
permintaan = {"Semarang": 90, "Yogyakarta": 170, "Solo": 120, "Tuban": 110, "Madiun": 70, "Banyuwangi": 80}

# Matriks Biaya Unit (Cij)
# Gunakan 999 untuk rute yang tidak tersedia/tidak ekonomis
M = 999 
biaya = {
    "Kudus": {"Semarang": 26.90, "Yogyakarta": 33.55, "Solo": M, "Tuban": M, "Madiun": M, "Banyuwangi": M},
    "Surabaya": {"Semarang": M, "Yogyakarta": M, "Solo": 43.40, "Tuban": 43.55, "Madiun": M, "Banyuwangi": M},
    "Malang": {"Semarang": M, "Yogyakarta": M, "Solo": M, "Tuban": 48.20, "Madiun": 30.25, "Banyuwangi": M},
    "Blitar": {"Semarang": M, "Yogyakarta": 52.85, "Solo": M, "Tuban": 35.70, "Madiun": M, "Banyuwangi": 28.57},
    "Kediri": {"Semarang": M, "Yogyakarta": 34.10, "Solo": M, "Tuban": 36.90, "Madiun": M, "Banyuwangi": M}
}

# 2. Inisiasi Model LP (Minimasi Biaya)
model = pulp.LpProblem("Model_Transportasi_Perusahaan_X", pulp.LpMinimize)

# 3. Definisikan Variabel Keputusan (Xij)
# Xij = Jumlah unit yang dikirim dari gudang i ke toko j
rute = [(i, j) for i in gudang for j in toko]
x = pulp.LpVariable.dicts("Alokasi", rute, lowBound=0, cat='Integer')

# 4. Fungsi Tujuan
# Min Z = Sum (Cij * Xij)
model += pulp.lpSum([x[i, j] * biaya[i][j] for i, j in rute]), "Biaya_Total_Minimum"

# 5. Kendala (Constraints)

# Kendala Kapasitas (Supply) - Sum Xij <= Kapasitas
for i in gudang:
    model += pulp.lpSum([x[i, j] for j in toko]) <= kapasitas[i], f"Kapasitas_Gudang_{i}"

# Kendala Permintaan (Demand) - Sum Xij = Permintaan (Karena model seimbang)
for j in toko:
    model += pulp.lpSum([x[i, j] for i in gudang]) == permintaan[j], f"Permintaan_Toko_{j}"

# 6. Selesaikan Model
model.solve()

# 7. Tampilkan Hasil
print(f"Status Solusi: {pulp.LpStatus[model.status]}")
print(f"Biaya Total Minimum (Z): Rp {pulp.value(model.objective):,.2f}\n")

print("Alokasi Optimal (Xij):")
tabel_hasil = []
for i in gudang:
    for j in toko:
        if x[i, j].varValue > 0:
            alokasi = int(x[i, j].varValue)
            biaya_unit = biaya[i][j]
            biaya_rute = alokasi * biaya_unit
            tabel_hasil.append({
                "Gudang": i, 
                "Toko": j, 
                "Unit": alokasi, 
                "Biaya Unit": f"Rp {biaya_unit:,.2f}",
                "Biaya Rute": f"Rp {biaya_rute:,.2f}"
            })

# Format output hasil
import pandas as pd
df_hasil = pd.DataFrame(tabel_hasil)
print(df_hasil.to_markdown(index=False))