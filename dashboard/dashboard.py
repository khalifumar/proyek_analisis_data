import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({'font.size': 12, 'axes.titlesize': 14, 'axes.labelsize': 12})

sns.set_palette("Set2")  # Pilih palet warna yang lebih lembut dan kontras

plt.xticks(rotation=45)  # Rotasi label X agar tidak tumpang tindih


# Fungsi untuk memuat data
def load_data():
    # Load hour.csv
    hour_df = pd.read_csv("hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    # Load day.csv
    day_df = pd.read_csv("day.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # Mapping kolom untuk kedua dataset
    season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Badai"}

    hour_df['season'] = hour_df['season'].map(season_mapping)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_mapping)

    day_df['season'] = day_df['season'].map(season_mapping)
    day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)

    return hour_df, day_df

# Memuat data
hour_df, day_df = load_data()

# Bagian Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")
st.sidebar.title("Pengaturan")
st.sidebar.markdown("Gunakan opsi ini untuk memfilter data")

# Pilihan dataset
dataset_choice = st.sidebar.selectbox(
    "Pilih Dataset",
    options=["Per Jam (hour.csv)", "Per Hari (day.csv)"]
)

# Filter berdasarkan musim
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"],
    default=["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
)

# Filter berdasarkan cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=["Cerah", "Mendung", "Hujan", "Badai"],
    default=["Cerah", "Mendung", "Hujan", "Badai"]
)

# Pilih dataset berdasarkan pilihan
if dataset_choice == "Per Jam (hour.csv)":
    df = hour_df
else:
    df = day_df

# Terapkan filter
filtered_data = df[
    (df['season'].isin(season_filter)) &
    (df['weathersit'].isin(weather_filter))
]

# Tampilkan data yang difilter
st.markdown("### Data yang Difilter")
st.dataframe(filtered_data)

# Statistik Deskriptif
st.markdown("### Statistik Deskriptif")
st.write(filtered_data.describe())




# Visualisasi 1: Tren Penggunaan Sepeda Berdasarkan Musim
tab1, tab2 = st.tabs(["Visualisas", "Keterangan"])

with tab1:
    st.markdown("### Tren Penggunaan Sepeda Berdasarkan Musim")
    plt.figure(figsize=(14, 7))  # Ukuran grafik yang lebih besar
    sns.set(style="whitegrid")
    line_plot = sns.lineplot(data=filtered_data, x='dteday', y='cnt', hue='season', palette='Set2', linewidth=2)
    line_plot.set_title("Tren Penggunaan Sepeda Berdasarkan Musim", fontsize=16)
    line_plot.set_xlabel("Tanggal", fontsize=12)
    line_plot.set_ylabel("Jumlah Penggunaan Sepeda", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)

with tab2:
    st.markdown("**Keterangan:**")
    
    col1, col2 = st.columns(2)


    # Menampilkan keterangan berdasarkan musim yang dipilih
    with col1:
        if "Musim Panas" in season_filter:
            st.write("#### Musim Panas")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada musim panas. Pada musim ini, biasanya ada peningkatan penggunaan sepeda karena cuaca yang lebih panas.")
        if "Musim Semi" in season_filter:
            st.write("#### Musim Semi")        
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada musim semi. Cuaca pada musim semi cenderung lebih sejuk dan mendukung aktivitas luar ruangan.")
        if "Musim Gugur" in season_filter:
            st.write("#### Musim Gugur")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada musim gugur. Musim ini bisa membawa cuaca yang lebih sejuk dengan kemungkinan hujan.")
        if "Musim Dingin" in season_filter:
            st.write("#### Musim Dingin")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada musim dingin. Penggunaan sepeda biasanya lebih rendah karena cuaca yang lebih dingin dan tidak nyaman.")
    
    # Menampilkan keterangan berdasarkan cuaca yang dipilih
    with col2:
        if "Cerah" in weather_filter:
            st.write("#### Cuaca Cerah")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada kondisi cuaca cerah. Pengguna sepeda lebih banyak saat cuaca cerah dan mendukung aktivitas luar ruangan.")
        if "Mendung" in weather_filter:
            st.write("#### Cuaca Mendung")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada kondisi cuaca mendung. Cuaca mendung dapat mempengaruhi minat untuk bersepeda, namun masih banyak yang menggunakan sepeda.")
        if "Hujan" in weather_filter:
            st.write("#### Cuaca Hujan")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada kondisi hujan. Cuaca hujan dapat menyebabkan penurunan penggunaan sepeda karena kurang nyaman dan risiko tergelincir.")
        if "Badai" in weather_filter:
            st.write("#### Cuaca Badai")
            st.write("Data yang ditampilkan menunjukkan penggunaan sepeda pada kondisi badai. Biasanya, penggunaan sepeda sangat menurun dalam kondisi badai.")


# Visualisasi 2: Distribusi Penggunaan Sepeda Berdasarkan Cuaca
tab3, tab4 = st.tabs(["Visualisasi", "Keterangan"])

with tab3:
    st.markdown("### Distribusi Penggunaan Sepeda Berdasarkan Cuaca")
    plt.figure(figsize=(14, 7))  # Ukuran grafik yang lebih besar
    sns.set(style="whitegrid")
    box_plot = sns.boxplot(x='weathersit', y='cnt', data=filtered_data, palette='Set2', linewidth=1.5)
    box_plot.set_title("Distribusi Penggunaan Sepeda Berdasarkan Cuaca", fontsize=16)
    box_plot.set_xlabel("Kondisi Cuaca", fontsize=12)
    box_plot.set_ylabel("Jumlah Penggunaan Sepeda", fontsize=12)
    st.pyplot(plt)

with tab4:
    st.markdown("**Keterangan:**")

    # Menyesuaikan keterangan berdasarkan dataset dan filter
    if dataset_choice == "Per Jam (hour.csv)":
        st.write("Grafik ini menunjukkan distribusi penggunaan sepeda berdasarkan kondisi cuaca pada dataset per jam. Cuaca yang lebih buruk (seperti hujan atau badai) cenderung mengurangi penggunaan sepeda. Dan sebaliknya cuaca yang cerah cenderung memicu penggunaan sepeda.")
    else:
        st.write("Grafik ini menunjukkan distribusi penggunaan sepeda berdasarkan kondisi cuaca pada dataset per hari. Penggunaan sepeda biasanya berkurang saat cuaca buruk.")


# Visualisasi 3: Tren Penggunaan Sepeda Berdasarkan Hari Minggu (Khusus day.csv)
if dataset_choice == "Per Hari (day.csv)":  # Hanya tampilkan tab ini untuk 'day.csv'
    tab5, tab6 = st.tabs(["Visualisasi", "Penjelasan"])

    with tab5:
        st.markdown("### Tren Penggunaan Sepeda Berdasarkan Hari Minggu")
        plt.figure(figsize=(10, 5))
        sns.barplot(x='weekday', y='cnt', data=filtered_data, ci=None)
        plt.title("Penggunaan Sepeda Berdasarkan Hari Minggu")
        plt.xlabel("Hari dalam Seminggu")
        plt.ylabel("Jumlah Penggunaan Sepeda")
        st.pyplot(plt)

    with tab6:
        st.markdown("**Keterangan**")
        st.write("Pada visualisasi ini, kita dapat melihat distribusi penggunaan sepeda berdasarkan hari dalam seminggu. Berdasarkan data, dapat terlihat apakah penggunaan sepeda lebih tinggi pada hari kerja atau akhir pekan.")
        st.write("Jika Anda melihat penggunaan yang lebih tinggi pada akhir pekan, ini bisa jadi karena orang lebih cenderung menggunakan sepeda untuk rekreasi atau olahraga pada hari libur.")


# Visualisasi 4: Tren Penggunaan Sepeda saat Cuaca Tidak Stabil

