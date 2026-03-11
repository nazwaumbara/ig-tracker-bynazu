import streamlit as st
import json
import os
import pandas as pd
import time

# ==========================================
# BAGIAN 1: BACKEND (Mesin Pemroses Data)
# ==========================================
def ekstrak_username(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    daftar_nama = set()
    
    def cari_nama(obj):
        if isinstance(obj, dict):
            if "string_list_data" in obj:
                for item in obj["string_list_data"]:
                    if "value" in item:
                        daftar_nama.add(item["value"])
                    elif "title" in obj and obj["title"] != "":
                        daftar_nama.add(obj["title"])
            for kunci, isi in obj.items():
                cari_nama(isi)
        elif isinstance(obj, list):
            for item in obj:
                cari_nama(item)
                
    cari_nama(data)
    return daftar_nama

# ==========================================
# BAGIAN 2: UI (Tampilan Aplikasi Depan)
# ==========================================
# Layout diatur lebih rapi
st.set_page_config(page_title="Instagram Tracker", page_icon="🕵️", layout="centered")

# Membuat Sidebar Minimalis di sebelah kiri
with st.sidebar:
    st.header("⚙️ Status Sistem")
    st.write("Pastikan file JSON sudah berada di folder yang tepat.")
    st.caption("🔒 Berjalan 100% lokal (Offline). Data kamu aman.")

st.title("🕵️ Detektif Instagram")
st.markdown("Cari tahu siapa yang tidak *follback* kamu dengan antarmuka yang bersih dan rapi.")
st.divider() # Garis pembatas modern

jalur_followers = "followers_and_following_nazu/followers_1.json"
jalur_following = "followers_and_following_nazu/following.json"

# ==========================================
# BAGIAN 3: AKSI
# ==========================================
# Mengubah tombol menjadi warna utama (primary) agar mencolok
if st.button("Mulai Analisis Data 🚀", use_container_width=True, type="primary"):
    
    if os.path.exists(jalur_followers) and os.path.exists(jalur_following):
        
        # Menambahkan animasi loading agar UI terasa matang
        with st.spinner('Detektif sedang memeriksa dokumen...'):
            time.sleep(1) # Memberi jeda 1 detik agar animasi terlihat (opsional)
            
            set_followers = ekstrak_username(jalur_followers)
            set_following = ekstrak_username(jalur_following)
            tidak_follback = set_following - set_followers
            
        if len(set_followers) == 0 or len(set_following) == 0:
            st.error("Gagal membaca nama. Format file JSON mungkin berbeda.")
        else:
            # 1. TAMPILAN METRIK MODERN
            st.subheader("📊 Ringkasan Akun")
            kolom1, kolom2, kolom3 = st.columns(3)
            # st.metric membuat angka besar dan rapi seperti dashboard profesional
            kolom1.metric(label="Pengikut (Followers)", value=len(set_followers))
            kolom2.metric(label="Mengikuti (Following)", value=len(set_following))
            kolom3.metric(label="Tidak Follback", value=len(tidak_follback), delta="- Evaluasi", delta_color="inverse")
            
            st.divider()
            
            # 2. TAMPILAN TABEL INTERAKTIF
            if len(tidak_follback) > 0:
                st.subheader("📝 Daftar Akun Tidak Follback")
                
                # Mengubah data mentah menjadi bentuk Tabel (Dataframe Pandas)
                df_hasil = pd.DataFrame({
                    "Username Instagram": sorted(list(tidak_follback))
                })
                # Membuat nomor urut tabel dimulai dari 1 (bukan 0)
                df_hasil.index = df_hasil.index + 1 
                
                # Menampilkan tabel interaktif
                st.dataframe(df_hasil, use_container_width=True, height=400)
                
                # Menambahkan sedikit efek perayaan di layar
                st.balloons()
    else:
        st.error("Ups! Gagal menemukan file JSON di folder 'followers_and_following'.")