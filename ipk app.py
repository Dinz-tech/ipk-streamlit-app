import streamlit as st

# CSS untuk background tema pantai
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Inisialisasi session_state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'matkul_data' not in st.session_state:
    st.session_state.matkul_data = []
if 'riwayat_mahasiswa' not in st.session_state:
    st.session_state.riwayat_mahasiswa = []

# Halaman 1: Input Data Mahasiswa
if st.session_state.page == 1:
    st.title("📘 Input Data Mahasiswa")

    nama = st.text_input("Nama Mahasiswa")
    nim = st.text_input("NIM")
    jumlah_matkul = st.number_input("Jumlah Mata Kuliah", min_value=1, step=1)

    if 'matkul_info' not in st.session_state or len(st.session_state.matkul_info) != int(jumlah_matkul):
        st.session_state.matkul_info = [{} for _ in range(int(jumlah_matkul))]

    st.subheader("📚 Data Mata Kuliah")
    for i in range(int(jumlah_matkul)):
        st.session_state.matkul_info[i]['nama_matkul'] = st.text_input(f"Nama Mata Kuliah {i+1}", key=f"matkul_{i}")
        st.session_state.matkul_info[i]['dosen'] = st.text_input(f"Nama Dosen {i+1}", key=f"dosen_{i}")
        st.session_state.matkul_info[i]['sks'] = st.number_input(f"SKS {i+1}", min_value=1, max_value=6, step=1, key=f"sks_{i}")

    if st.button("Lanjut ke Input Nilai"):
        st.session_state.nama = nama
        st.session_state.nim = nim
        st.session_state.jumlah_matkul = jumlah_matkul
        st.session_state.page = 2
        st.rerun()

# Halaman 2: Input Nilai
elif st.session_state.page == 2:
    st.title("📝 Input Nilai Per Mata Kuliah")

    ipk_total = 0
    total_sks = 0
    rekap_data = []

    for i in range(int(st.session_state.jumlah_matkul)):
        st.subheader(f"Mata Kuliah {i+1}: {st.session_state.matkul_info[i]['nama_matkul']}")

        absen = st.number_input("Nilai Absen (maks. 10)", min_value=0.0, max_value=10.0, key=f"absen_{i}")
        tugas = st.number_input("Nilai Tugas (maks. 20)", min_value=0.0, max_value=20.0, key=f"tugas_{i}")
        uts = st.number_input("Nilai UTS (maks. 30)", min_value=0.0, max_value=30.0, key=f"uts_{i}")
        uas = st.number_input("Nilai UAS (maks. 40)", min_value=0.0, max_value=40.0, key=f"uas_{i}")

        total_nilai = absen + tugas + uts + uas
        ipk = (total_nilai / 100) * 4

        if ipk >= 3.50:
            predikat = "A"
        elif ipk >= 3.00:
            predikat = "B"
        elif ipk >= 2.50:
            predikat = "C"
        elif ipk >= 2.00:
            predikat = "D"
        else:
            predikat = "E"

        sks = st.session_state.matkul_info[i]['sks']
        ipk_total += ipk * sks
        total_sks += sks

        rekap_data.append({
            "Mata Kuliah": st.session_state.matkul_info[i]['nama_matkul'],
            "Dosen": st.session_state.matkul_info[i]['dosen'],
            "SKS": sks,
            "Nilai (100)": total_nilai,
            "IPK": round(ipk, 2),
            "Predikat": predikat
        })

    if st.button("🎓 Hitung IPK Akhir"):
        ipk_akhir = ipk_total / total_sks if total_sks > 0 else 0

        st.markdown("---")
        st.subheader("📊 Rekap Nilai Seluruh Mata Kuliah")
        st.dataframe(rekap_data)

        st.markdown(f"### 👤 Nama: `{st.session_state.nama}`")
        st.markdown(f"### 🆔 NIM: `{st.session_state.nim}`")
        st.markdown(f"### 📌 Total SKS: `{total_sks}`")
        st.markdown(f"### 🎯 IPK Akhir (Berbobot SKS): `{ipk_akhir:.2f}`")

    if st.button("💾 Simpan & Tambah Mahasiswa Baru"):
        st.session_state.riwayat_mahasiswa.append({
            "nama": st.session_state.nama,
            "nim": st.session_state.nim,
            "total_sks": total_sks,
            "ipk_akhir": round(ipk_total / total_sks, 2) if total_sks > 0 else 0,
            "rekap": rekap_data
        })
        # Reset ke halaman awal
        st.session_state.page = 1
        st.session_state.matkul_info = []
        st.session_state.jumlah_matkul = 1
        st.rerun()

    if st.button("🔙 Kembali ke Halaman 1"):
        st.session_state.page = 1
        st.rerun()

# Menampilkan Riwayat Mahasiswa
if st.session_state.riwayat_mahasiswa:
    st.markdown("---")
    st.subheader("📚 Riwayat Mahasiswa yang Sudah Diinput")
    for idx, mhs in enumerate(st.session_state.riwayat_mahasiswa, start=1):
        st.markdown(f"### {idx}. {mhs['nama']} ({mhs['nim']})")
        st.markdown(f"- Total SKS: `{mhs['total_sks']}`")
        st.markdown(f"- IPK Akhir: `{mhs['ipk_akhir']}`")
        st.markdown("**Rekap Mata Kuliah:**")
        st.dataframe(mhs['rekap'])