import pandas as pd
import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Keuangan Daerah",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Styling Tema Warna Kustom (#91AE6E & #D96868)
st.markdown(
    """
    <style>
        /* Warna Latar Belakang */
        .main {
            background-color: #f7f9f5;
        }
        
        /* Card Metrik Aksen Sage Green (#91AE6E) & Terracotta (#D96868) */
        div.stMetric {
            background-color: #ffffff;
            padding: 18px;
            border-radius: 12px;
            border-left: 5px solid #91AE6E;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        div.stMetric label {
            color: #58713a !important;
            font-weight: 600;
        }
        div.stMetric [data-testid="stMetricValue"] {
            color: #2c3820 !important;
        }

        /* Custom Header Styling */
        .title-text {
            color: #91AE6E;
            font-weight: 700;
            margin-bottom: 0px;
        }
        .subtitle-text {
            color: #D96868;
            font-weight: 500;
            margin-bottom: 25px;
        }

        /* Tombol Unduh / Action Button */
        div.stButton > button {
            background-color: #D96868 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
        }
        div.stButton > button:hover {
            background-color: #b84f4f !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. Mendaftar Data Dummy Sesuai Struktur
@st.cache_data
def load_data():
  data = {
      "Kota": [
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Banda Aceh",
          "Kota Sabang",
          "Kota Sabang",
          "Kota Sabang",
          "Kota Sabang",
          "Kota Sabang",
      ],
      "Tahun": [
          2016,
          2017,
          2018,
          2019,
          2020,
          2021,
          2022,
          2023,
          2024,
          2020,
          2021,
          2022,
          2023,
          2024,
      ],
      "DBH_Pajak": [
          78.91,
          72.77,
          93.06,
          92.60,
          97.36,
          102.50,
          81.18,
          115.08,
          67.16,
          25.27,
          28.10,
          30.45,
          35.12,
          32.80,
      ],
      "DBH_SDA": [
          27.08,
          26.01,
          82.81,
          29.52,
          58.70,
          83.44,
          72.27,
          97.74,
          50.23,
          15.74,
          18.20,
          22.15,
          25.80,
          21.10,
      ],
      "DBH_Lainnya": [
          39.83,
          46.46,
          31.70,
          51.04,
          34.77,
          49.04,
          35.37,
          70.87,
          58.26,
          8.25,
          10.15,
          12.30,
          14.50,
          11.90,
      ],
      "DAU_Grant": [
          107.56,
          109.93,
          127.89,
          142.44,
          107.83,
          165.62,
          119.55,
          173.29,
          139.33,
          35.77,
          38.90,
          42.10,
          45.60,
          41.20,
      ],
      "DAU_Earmark": [
          52.78,
          80.91,
          60.87,
          61.59,
          68.51,
          93.72,
          74.24,
          82.99,
          91.09,
          29.95,
          31.20,
          34.50,
          38.10,
          36.40,
      ],
      "DAK_Fisik": [
          96.10,
          63.40,
          77.20,
          51.80,
          69.30,
          67.10,
          66.50,
          92.40,
          102.10,
          19.80,
          21.50,
          23.10,
          27.40,
          25.80,
      ],
  }
  return pd.DataFrame(data)


df = load_data()

# 4. Sidebar Filter
st.sidebar.markdown(
    "<h2 style='color: #91AE6E;'>🌿 Filter Data</h2>", unsafe_allow_html=True
)

# Filter Kota
kota_options = df["Kota"].unique().tolist()
selected_kota = st.sidebar.multiselect(
    "Pilih Kota/Kabupaten:", kota_options, default=kota_options
)

# Filter Rentang Tahun
min_year = int(df["Tahun"].min())
max_year = int(df["Tahun"].max())
selected_years = st.sidebar.slider(
    "Rentang Tahun:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

# Terapkan Filter
df_filtered = df[
    (df["Kota"].isin(selected_kota))
    & (df["Tahun"] >= selected_years[0])
    & (df["Tahun"] <= selected_years[1])
]

# 5. Header Utama
st.markdown(
    "<h1 class='title-text'>📊 Dashboard Keuangan Daerah</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtitle-text'>Analisis Alokasi Dana Bagi Hasil (DBH), DAU, dan"
    " DAK Daerah</p>",
    unsafe_allow_html=True,
)

if df_filtered.empty:
  st.warning("⚠️ Data tidak ditemukan untuk filter yang dipilih.")
else:
  # 6. Ringkasan Metrik (KPIs)
  col1, col2, col3, col4 = st.columns(4)

  total_dbh_pajak = df_filtered["DBH_Pajak"].sum()
  total_dbh_sda = df_filtered["DBH_SDA"].sum()
  total_dau = df_filtered["DAU_Grant"].sum() + df_filtered["DAU_Earmark"].sum()
  total_dak = df_filtered["DAK_Fisik"].sum()

  with col1:
    st.metric("Total DBH Pajak", f"{total_dbh_pajak:,.2f} M")
  with col2:
    st.metric("Total DBH SDA", f"{total_dbh_sda:,.2f} M")
  with col3:
    st.metric("Total DAU", f"{total_dau:,.2f} M")
  with col4:
    st.metric("Total DAK Fisik", f"{total_dak:,.2f} M")

  st.markdown("<br>", unsafe_allow_html=True)

  # 7. Visualisasi Tren Grafik (Menggunakan Warna Kustom #91AE6E & #D96868)
  col_chart1, col_chart2 = st.columns(2)

  with col_chart1:
    st.subheader("📈 Tren DBH Pajak & SDA Berdasarkan Tahun")
    df_trend = df_filtered.groupby("Tahun")[
        ["DBH_Pajak", "DBH_SDA", "DBH_Lainnya"]
    ].sum()
    # Menggunakan palet warna kustom pada chart
    st.line_chart(df_trend, color=["#91AE6E", "#D96868", "#C3D4A4"])

  with col_chart2:
    st.subheader("📊 Perbandingan DAU & DAK Fisik")
    df_dau_dak = df_filtered.groupby("Tahun")[
        ["DAU_Grant", "DAU_Earmark", "DAK_Fisik"]
    ].sum()
    st.bar_chart(df_dau_dak, color=["#D96868", "#91AE6E", "#E3A1A1"])

  st.divider()

  # 8. Tabel Data Interaktif
  st.subheader("📋 Data Detail Transaksi Daerah")

  st.dataframe(df_filtered, use_container_width=True, hide_index=True)

  # Fitur Download CSV
  csv = df_filtered.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Unduh Data CSV",
      data=csv,
      file_name="data_keuangan_daerah.csv",
      mime="text/csv",
  )
