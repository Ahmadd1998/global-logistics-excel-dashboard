'''
import streamlit as st
import pandas as pd

# =====================================================================
# [VERSI AKTIF] - LEVEL 2 (SESUAI GAMBAR TERAKHIR)
# Ini yang bakal jalan dan dibaca sama server Streamlit malam ini.
# =====================================================================

# 1. KONFIGURASI HALAMAN DASHBOARD
st.set_page_config(page_title="Logistics & Carrier Performance", page_icon="📦", layout="wide")

st.title("📦 Logistics & Carrier Performance Dashboard")
st.markdown("**Data Operations & Operational Analytics — Portfolio Project**")
st.write("---")

# 2. FUNGSI LOAD DATA
@st.cache_data
def load_data():
    df_cust = pd.read_csv('customer.xlsx - customer.csv')
    df_perf = pd.read_csv('customer.xlsx - logistics_performance.csv')
    df_ship = pd.read_csv('customer.xlsx - shipment.csv')
    return df_cust, df_perf, df_ship

try:
    df_cust, df_perf, df_ship = load_data()
    
    # 3. KARTU METRIK RINGKASAN
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👥 Total Registrasi Customer", value=f"{len(df_cust)} Users")
    with col2:
        st.metric(label="🚢 Total Shipment Logs", value=f"{len(df_ship)} Pengiriman")
    with col3:
        st.metric(label="📊 Carrier Performance Records", value=f"{len(df_perf)} Entri")
    
    st.write("---")
    
    # 4. TAB NAVIGASI INTERAKTIF
    st.markdown("### 🗂️ Eksplorasi Data Base Logistik")
    tab1, tab2, tab3 = st.tabs(["👥 Profil Customer", "📊 Kinerja Carrier (Vendor)", "🚢 Manifes Pengiriman"])
    
    with tab1:
        st.subheader("Data Demografi & Profil Pelanggan")
        search_query = st.text_input("🔍 Cari Customer (Ketik sesuatu lalu Enter):", "")
        if search_query:
            mask = df_cust.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df_cust[mask], use_container_width=True)
        else:
            st.dataframe(df_cust, use_container_width=True)
        
    with tab2:
        st.subheader("Analisis Performa Waktu & Kerusakan Vendor Ekspedisi")
        carrier_col = [col for col in df_perf.columns if 'carrier' in col.lower()]
        if carrier_col:
            col_name = carrier_col[0]
            selected_carrier = st.selectbox("📌 Pilih Vendor Logistik (Carrier):", ["Semua Vendor"] + list(df_perf[col_name].unique()))
            if selected_carrier != "Semua Vendor":
                filtered_perf = df_perf[df_perf[col_name] == selected_carrier]
            else:
                filtered_perf = df_perf
            st.dataframe(filtered_perf, use_container_width=True)
            
            st.markdown("#### 📈 Visualisasi Transaksi per Vendor")
            chart_data = df_perf[col_name].value_counts()
            st.bar_chart(chart_data)
        else:
            st.dataframe(df_perf, use_container_width=True)
            
    with tab3:
        st.subheader("Detail Logistik Barang Lintas Wilayah")
        status_col = [col for col in df_ship.columns if 'status' in col.lower()]
        if status_col:
            s_col = status_col[0]
            statuses = df_ship[s_col].dropna().unique()
            selected_status = st.multiselect("🎯 Filter Status Pengiriman:", statuses, default=statuses)
            st.dataframe(df_ship[df_ship[s_col].isin(selected_status)], use_container_width=True)
        else:
            st.dataframe(df_ship, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Eror: File CSV tidak ditemukan. Pastikan 3 file CSV sudah diupload!")

st.write("---")
st.caption("Logistics Dashboard System | Developed by Ahmad Gozali Abbas")
'''

# =====================================================================
# [VERSI CADANGAN] - FINAL BOSS LEVEL (FULL DIAGRAM)
# Kumpulan kode di bawah ini TIDAK AKAN JALAN karena diapit tanda '''
# Kalau besok mau dipakai, tinggal hapus tanda ''' di atas dan di bawah kode ini,
# lalu berikan tanda ''' pada versi aktif di atas.
# =====================================================================
'''
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistics & Carrier Performance", page_icon="📦", layout="wide")
st.title("📦 Logistics & Carrier Performance Dashboard")
st.markdown("**Data Operations & Operational Analytics — Portfolio Project**")
st.write("---")

@st.cache_data
def load_data():
    df_cust = pd.read_csv('dataset/customer.xlsx - customer.csv')
    df_perf = pd.read_csv('dataset/customer.xlsx - logistics_performance.csv')
    df_ship = pd.read_csv('dataset/customer.xlsx - shipment.csv')
    return df_cust, df_perf, df_ship

try:
    df_cust, df_perf, df_ship = load_data()
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("👥 Total Registrasi Customer", f"{len(df_cust)} Users")
    with col2: st.metric("🚢 Total Shipment Logs", f"{len(df_ship)} Pengiriman")
    with col3: st.metric("📊 Carrier Performance Records", f"{len(df_perf)} Entri")
    st.write("---")
    
    st.markdown("### 🗂️ Eksplorasi Data Base Logistik")
    tab1, tab2, tab3 = st.tabs(["👥 Profil Customer", "📊 Kinerja Carrier (Vendor)", "🚢 Manifes Pengiriman"])
    
    with tab1:
        st.subheader("Data Demografi & Profil Pelanggan")
        search_query = st.text_input("🔍 Cari Customer (Ketik Nama/ID):", "")
        if search_query:
            mask = df_cust.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df_cust[mask], use_container_width=True)
        else:
            st.dataframe(df_cust, use_container_width=True)
            
        country_col = [col for col in df_cust.columns if 'country' in col.lower() or 'negara' in col.lower()]
        if country_col:
            st.markdown("#### 🌍 Distribusi Pelanggan Berdasarkan Negara")
            st.bar_chart(df_cust[country_col[0]].value_counts())
        
    with tab2:
        st.subheader("Analisis Performa Waktu & Kerusakan Vendor Ekspedisi")
        carrier_col = [col for col in df_perf.columns if 'carrier' in col.lower()]
        if carrier_col:
            col_name = carrier_col[0]
            selected_carrier = st.selectbox("📌 Pilih Vendor Logistik:", ["Semua Vendor"] + list(df_perf[col_name].unique()))
            filtered_perf = df_perf[df_perf[col_name] == selected_carrier] if selected_carrier != "Semua Vendor" else df_perf
            st.dataframe(filtered_perf, use_container_width=True)
            
            st.markdown("#### 📉 Komparasi Performa (Numerik) Antar Vendor")
            numeric_cols = df_perf.set_index(col_name).select_dtypes(include=['float64', 'int64'])
            if not numeric_cols.empty: st.line_chart(numeric_cols)
        else:
            st.dataframe(df_perf, use_container_width=True)
            
    with tab3:
        st.subheader("Detail Logistik Barang Lintas Wilayah")
        status_col = [col for col in df_ship.columns if 'status' in col.lower()]
        if status_col:
            s_col = status_col[0]
            statuses = df_ship[s_col].dropna().unique()
            selected_status = st.multiselect("🎯 Filter Status Pengiriman:", statuses, default=statuses)
            st.dataframe(df_ship[df_ship[s_col].isin(selected_status)], use_container_width=True)
            
            st.markdown("#### 📊 Rasio Status Pengiriman Keseluruhan")
            st.bar_chart(df_ship[s_col].value_counts())
        else:
            st.dataframe(df_ship, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Eror: File CSV tidak ditemukan.")

st.write("---")
st.caption("Logistics Dashboard System | Developed by Ahmad Gozali Abbas")
'''
import streamlit as st
import pandas as pd
import os

# ================================================
# LOGISTICS & CARRIER PERFORMANCE DASHBOARD
# ================================================

st.set_page_config(
    page_title="Logistics & Carrier Performance",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Logistics & Carrier Performance Dashboard")
st.markdown("**Data Operations & Operational Analytics — Portfolio Project**")
st.caption("Developed by Ahmad Gozali Abbas")

# Load Data dari folder dataset
@st.cache_data
def load_data():
    try:
        base_path = "dataset"
        
        df_cust = pd.read_csv(os.path.join(base_path, "customer.xlsx - customer.csv"))
        df_perf = pd.read_csv(os.path.join(base_path, "customer.xlsx - logistics_performance.csv"))
        df_ship = pd.read_csv(os.path.join(base_path, "customer.xlsx - shipment.csv"))
        
        return df_cust, df_perf, df_ship
    except FileNotFoundError as e:
        st.error(f"❌ File tidak ditemukan: {e}")
        st.info("Pastikan folder **dataset** berisi 3 file CSV di bawah ini:")
        st.code("""dataset/
├── customer.xlsx - customer.csv
├── customer.xlsx - logistics_performance.csv
└── customer.xlsx - shipment.csv""")
        st.stop()
    except Exception as e:
        st.error(f"Terjadi error: {e}")
        st.stop()

df_cust, df_perf, df_ship = load_data()

# ===================== METRIK =====================
st.write("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Registrasi Customer", f"{len(df_cust):,} Users")
with col2:
    st.metric("🚢 Total Shipment Logs", f"{len(df_ship):,} Pengiriman")
with col3:
    st.metric("📊 Carrier Performance Records", f"{len(df_perf):,} Entri")

st.write("---")

# ===================== TABS =====================
st.markdown("### 🗂️ Eksplorasi Data Base Logistik")
tab1, tab2, tab3 = st.tabs([
    "👥 Profil Customer", 
    "📊 Kinerja Carrier (Vendor)", 
    "🚢 Manifes Pengiriman"
])

# TAB 1: Customer
with tab1:
    st.subheader("Data Demografi & Profil Pelanggan")
    search_query = st.text_input("🔍 Cari Customer (Nama/ID):", "")
    
    if search_query:
        mask = df_cust.astype(str).apply(
            lambda x: x.str.contains(search_query, case=False)
        ).any(axis=1)
        filtered_df = df_cust[mask]
        st.dataframe(filtered_df, use_container_width=True)
        st.caption(f"Menampilkan {len(filtered_df)} hasil pencarian")
    else:
        st.dataframe(df_cust, use_container_width=True)

# TAB 2: Vendor Performance
with tab2:
    st.subheader("Analisis Performa Waktu & Kerusakan Vendor Ekspedisi")
    
    carrier_cols = [col for col in df_perf.columns if 'carrier' in col.lower()]
    carrier_col = carrier_cols[0] if carrier_cols else None
    
    if carrier_col:
        carriers = ["Semua Vendor"] + sorted(df_perf[carrier_col].astype(str).unique())
        selected_carrier = st.selectbox("📌 Pilih Vendor Logistik:", carriers)
        
        if selected_carrier != "Semua Vendor":
            filtered_perf = df_perf[df_perf[carrier_col] == selected_carrier]
        else:
            filtered_perf = df_perf
            
        st.dataframe(filtered_perf, use_container_width=True)
        
        st.markdown("#### 📈 Jumlah Pengiriman per Vendor")
        st.bar_chart(df_perf[carrier_col].value_counts())
    else:
        st.dataframe(df_perf, use_container_width=True)

# TAB 3: Shipments
with tab3:
    st.subheader("Detail Logistik Barang Lintas Wilayah")
    
    status_cols = [col for col in df_ship.columns if any(x in col.lower() for x in ['status', 'delivery'])]
    status_col = status_cols[0] if status_cols else None
    
    if status_col:
        statuses = sorted(df_ship[status_col].dropna().unique())
        selected_status = st.multiselect(
            "🎯 Filter Status Pengiriman:", 
            statuses, 
            default=statuses
        )
        
        filtered_ship = df_ship[df_ship[status_col].isin(selected_status)]
        st.dataframe(filtered_ship, use_container_width=True)
        
        st.markdown("#### 📊 Rasio Status Pengiriman Keseluruhan")
        st.bar_chart(df_ship[status_col].value_counts())
    else:
        st.dataframe(df_ship, use_container_width=True)

st.write("---")
st.caption("Logistics Dashboard System | Portfolio Project Ahmad Gozali Abbas")
