import streamlit as st
import pandas as pd
import os
import plotly.express as px

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Customer",
        value=f"{len(df_cust):,} Pelanggan"
    )

with col2:
    st.metric(
        label="🚢 Total Pengiriman",
        value=f"{len(df_ship):,} Pengiriman"
    )

with col3:
    if 'df_ship' in locals() and len(df_ship) > 0:
        status_cols = [col for col in df_ship.columns if any(x in col.lower() for x in ['status', 'delivery'])]
        status_col = status_cols[0] if status_cols else None
        if status_col:
            on_time_rate = (df_ship[status_col].value_counts().get("On-Time", 0) / len(df_ship) * 100)
            st.metric(
                label="✅ On-Time Rate",
                value=f"{on_time_rate:.1f}%",
                delta="Good" if on_time_rate > 80 else "Need Improvement"
            )
    else:
        st.metric("✅ On-Time Rate", "N/A")

with col4:
    delay_col = next((col for col in df_perf.columns if 'delay' in col.lower()), None)
    if delay_col:
        avg_delay = df_perf[delay_col].mean().round(1)
        st.metric("⏳ Avg Delay", f"{avg_delay} Jam")
    else:
        st.metric("📊 Record Vendor", f"{len(df_perf):,} Record")

st.write("---")

# ===================== TABS =====================
st.markdown("### 🗂️ Eksplorasi Data Base Logistik")
tab1, tab2, tab3 = st.tabs([
    "👥 Profil Customer",
    "📊 Kinerja Carrier (Vendor)",
    "🚢 Manifes Pengiriman"
])

with tab1:
    st.subheader("Data Demografi & Profil Pelanggan")
    search_query = st.text_input("🔍 Cari Customer (Nama/ID):", "").strip()
    
    if search_query:
        # Cleaning search query (lebih fleksibel)
        clean_query = search_query.replace("-", "").replace("_", "").lower()
        
        # Search lebih pintar
        mask = (
            df_cust.astype(str).apply(
                lambda x: x.str.replace("-", "").str.replace("_", "").str.lower().str.contains(clean_query, case=False)
            ).any(axis=1)
        )
        
        filtered_df = df_cust[mask]
        
        if len(filtered_df) > 0:
            st.dataframe(filtered_df, use_container_width=True)
            st.success(f"✅ Menampilkan {len(filtered_df)} hasil pencarian")
        else:
            st.warning(f"❌ Tidak ditemukan customer dengan kata kunci **'{search_query}'**")
            st.info("Coba gunakan ID tanpa strip (contoh: cust100 atau CUST100)")
    else:
        st.dataframe(df_cust, use_container_width=True)
        st.caption(f"Total Customer: {len(df_cust)}")
        st.caption(f"Menampilkan {len(filtered_df if 'filtered_df' in locals() else df_cust)} baris data")

# ===================== TAB 2: KINERJA CARRIER =====================
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
        st.caption(f"Menampilkan {len(filtered_perf):,} baris data dari {len(df_perf)} total")
       
        # Bar Chart
        st.markdown("#### 📊 Jumlah Pengiriman per Vendor")
        fig1 = px.bar(
            df_perf[carrier_col].value_counts().reset_index(),
            x=carrier_col,
            y='count',
            color=carrier_col,
            title="Total Shipments per Carrier",
            labels={'count': 'Jumlah Pengiriman', carrier_col: 'Vendor'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig1.update_layout(height=420)
        st.plotly_chart(fig1, use_container_width=True)
       
        # Pie Chart
        st.markdown("#### 🥧 Proporsi Pengiriman per Vendor")
        fig2 = px.pie(
            df_perf[carrier_col].value_counts().reset_index(),
            names=carrier_col,
            values='count',
            title="Distribusi Persentase Pengiriman",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig2, use_container_width=True)


# ===================== TAB 3: MANIFEST PENGIRIMAN =====================
with tab3:
    st.subheader("Detail Logistik Barang Lintas Wilayah")
   
    status_cols = [col for col in df_ship.columns if any(x in col.lower() for x in ['status', 'delivery'])]
    status_col = status_cols[0] if status_cols else None
   
    if status_col:
        all_statuses = df_ship[status_col].unique()
        statuses = sorted([s for s in all_statuses if pd.notna(s)])
        status_options = statuses + ["(Kosong / Null)"]
        
        selected_status = st.multiselect(
            "🎯 Filter Status Pengiriman:", 
            status_options, 
            default=statuses
        )
        
        # Filter logic
        if "(Kosong / Null)" in selected_status:
            mask = df_ship[status_col].isna() | df_ship[status_col].isin([s for s in selected_status if s != "(Kosong / Null)"])
        else:
            mask = df_ship[status_col].isin(selected_status)
        
        filtered_ship = df_ship[mask]
        
        st.dataframe(filtered_ship, use_container_width=True)
        st.caption(f"Menampilkan {len(filtered_ship):,} baris data dari {len(df_ship)} total")
        
        # === GRAFIK (pakai filtered data) ===
        st.markdown("#### 📊 Rasio Status Pengiriman Keseluruhan")
        
        status_count = filtered_ship[status_col].value_counts(dropna=False).reset_index()
        status_count.columns = ['Status', 'Jumlah']
        status_count['Status'] = status_count['Status'].fillna("(Kosong)")
        
        fig3 = px.bar(
            status_count,
            x='Status',
            y='Jumlah',
            color='Status',
            title="On-Time vs Delayed",
            color_discrete_map={"On-Time": "#00cc96", "Delayed": "#ef553b", "(Kosong)": "#888888"},
            text='Jumlah'
        )
        fig3.update_layout(height=420)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("#### 🥧 Persentase Status Pengiriman")
        fig4 = px.pie(
            status_count,
            names='Status',
            values='Jumlah',
            title="Persentase Status Pengiriman",
            color_discrete_map={"On-Time": "#00cc96", "Delayed": "#ef553b", "(Kosong)": "#888888"}
        )
        st.plotly_chart(fig4, use_container_width=True)
        
st.write("---")
st.caption("Logistics Dashboard System | Portfolio Project Ahmad Gozali Abbas")
