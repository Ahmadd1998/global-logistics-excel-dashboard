import streamlit as st
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN DASHBOARD
# ==========================================
st.set_page_config(page_title="Logistics & Carrier Performance", page_icon="📦", layout="wide")

st.title("📦 Logistics & Carrier Performance Dashboard")
st.markdown("**Data Operations & Operational Analytics — Portfolio Project**")
st.write("---")

# ==========================================
# 2. FUNGSI LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df_cust = pd.read_csv('customer.xlsx - customer.csv')
    df_perf = pd.read_csv('customer.xlsx - logistics_performance.csv')
    df_ship = pd.read_csv('customer.xlsx - shipment.csv')
    return df_cust, df_perf, df_ship

try:
    df_cust, df_perf, df_ship = load_data()
    
    # ==========================================
    # 3. KARTU METRIK RINGKASAN DI BAGIAN ATAS
    # ==========================================
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👥 Total Registrasi Customer", value=f"{len(df_cust)} Users")
    with col2:
        st.metric(label="🚢 Total Shipment Logs", value=f"{len(df_ship)} Pengiriman")
    with col3:
        st.metric(label="📊 Carrier Performance Records", value=f"{len(df_perf)} Entri")
    
    st.write("---")
    
    # ==========================================
    # 4. TAB NAVIGASI INTERAKTIF
    # ==========================================
    st.markdown("### 🗂️ Eksplorasi Data Base Logistik")
    tab1, tab2, tab3 = st.tabs(["👥 Profil Customer", "📊 Kinerja Carrier (Vendor)", "🚢 Manifes Pengiriman"])
    
    # --- TAB 1: CUSTOMER (FITUR SEARCH) ---
    with tab1:
        st.subheader("Data Demografi & Profil Pelanggan")
        # Bikin kotak pencarian
        search_query = st.text_input("🔍 Cari Customer (Ketik sesuatu lalu Enter):", "")
        
        if search_query:
            # Filter baris yang mengandung kata yang dicari
            mask = df_cust.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df_cust[mask], use_container_width=True)
        else:
            st.dataframe(df_cust, use_container_width=True)
        
    # --- TAB 2: PERFORMANCE (FITUR FILTER & DIAGRAM) ---
    with tab2:
        st.subheader("Analisis Performa Waktu & Kerusakan Vendor Ekspedisi")
        
        # Cari kolom yang mengandung nama 'carrier' untuk filter
        carrier_col = [col for col in df_perf.columns if 'carrier' in col.lower()]
        
        if carrier_col:
            col_name = carrier_col[0]
            # Bikin opsi dropdown
            selected_carrier = st.selectbox("📌 Pilih Vendor Logistik (Carrier):", ["Semua Vendor"] + list(df_perf[col_name].unique()))
            
            if selected_carrier != "Semua Vendor":
                filtered_perf = df_perf[df_perf[col_name] == selected_carrier]
            else:
                filtered_perf = df_perf
            
            st.dataframe(filtered_perf, use_container_width=True)
            
            # --- DIAGRAM BATANG ---
            st.markdown("#### 📈 Visualisasi Transaksi per Vendor")
            chart_data = df_perf[col_name].value_counts()
            st.bar_chart(chart_data)
        else:
            st.dataframe(df_perf, use_container_width=True)
            
    # --- TAB 3: SHIPMENT (FITUR MULTI-FILTER) ---
    with tab3:
        st.subheader("Detail Logistik Barang Lintas Wilayah")
        
        # Cari kolom status untuk difilter
        status_col = [col for col in df_ship.columns if 'status' in col.lower()]
        if status_col:
            s_col = status_col[0]
            statuses = df_ship[s_col].dropna().unique()
            
            # Bikin kotak filter multi-pilihan
            selected_status = st.multiselect("🎯 Filter Status Pengiriman:", statuses, default=statuses)
            
            # Tampilkan dataframe sesuai status yang dipilih
            st.dataframe(df_ship[df_ship[s_col].isin(selected_status)], use_container_width=True)
        else:
            st.dataframe(df_ship, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Eror: File CSV tidak ditemukan. Pastikan 3 file CSV sudah diupload!")

st.write("---")
st.caption("Logistics Dashboard System | Developed by Ahmad Gozali Abbas")
