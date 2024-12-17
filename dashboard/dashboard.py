import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Dashboard Analisis Bike Sharing")

# Mengambil Data
day_df = pd.read_csv("dashboard/day.csv", delimiter=",")
hour_df = pd.read_csv("dashboard/hour.csv", delimiter=",")

# Sidebar untuk memilih dataset
dataset_option = st.sidebar.selectbox("Pilih Dataset:", ["Day", "Hour"])

if dataset_option == "Day":
    st.subheader("Dataset day.csv")
    df = day_df
else:
    st.subheader("Dataset hour.csv")
    df = hour_df

# Menampilkan seluruh data dari day_df dan hour_df
if dataset_option == "Day" :
    st.dataframe(hour_df, width=1000, height=500)
    day_df.rename(columns={'instant': 'id_pengguna'}, inplace=True)
else :
    st.dataframe(day_df, width=1000, height=500)
    hour_df.rename(columns={'instant': 'id_pengguna'}, inplace=True)


# Mapping Season
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
day_df['season'] = day_df['season'].map(season_mapping)
hour_df['season'] = hour_df['season'].map(season_mapping)

# Mapping Year
yr_mapping = {0: 2011, 1: 2012}
day_df['yr'] = day_df['yr'].map(yr_mapping)
hour_df['yr'] = hour_df['yr'].map(yr_mapping)

# Mapping Holiday
holiday_mapping = {0: "Tidak", 1: "Ya"}
day_df['holiday'] = day_df['holiday'].map(holiday_mapping)
hour_df['holiday'] = hour_df['holiday'].map(holiday_mapping)

# Mapping Weekday
weekday_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
day_df['weekday'] = day_df['weekday'].map(weekday_mapping)
hour_df['weekday'] = hour_df['weekday'].map(weekday_mapping)

# Mapping Workingday
workingday_mapping = {0: "Tidak", 1: "Ya"}
day_df['workingday'] = day_df['workingday'].map(workingday_mapping)
hour_df['workingday'] = hour_df['workingday'].map(workingday_mapping)

# Mapping Weathersit
weathersit_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Badai"}
day_df['weathersit'] = day_df['weathersit'].map(weathersit_mapping)
hour_df['weathersit'] = hour_df['weathersit'].map(weathersit_mapping)

st.header("Analisis Cuaca Berdasarkan Kolom Weather dan Cnt")
col1, col2 = st.columns(2, vertical_alignment="top")
with col1:
    # Analisis Cuaca
    st.subheader("Bar Chart Cuaca")
    weather_trend = df.groupby('weathersit')['cnt'].mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    weather_trend.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xlabel("Kondisi Cuaca")
    st.pyplot(fig)

with col2:
    st.subheader("Penjelasan")
    st.markdown("""
        Berdasarkan analisis jumlah pengguna sepeda dengan kondisi cuaca di tahun 2011 sampai dengan 2012, dibagi menjadi 3 cuaca, 
        yaitu Cerah, Mendung, dan Hujan. Dari ketiga cuaca tersebut, kondisi cuaca dengan pengguna sepeda paling banyak berada 
        pada kondisi Cerah. Dan kondisi cuaca dengan pengguna sepeda paling sedikiy berada pada kondisi Hujan. Hal tersebut 
        memamng secara naluri dan logika menggunakan sepeda sangat tepat karena pengguna sepeda akan merasakan nikmatnya menggunakan 
        sepeda di saat cuaca sedang cerah.
        
    """)

st.header("Analisis Jumlah Pengguna Berdasarkan Musim")
col3, col4 = st.columns(2)
with col3:
    # Analisis Data
    season_user_count = day_df.groupby('season')['cnt'].sum()

    # Menampilkan Data
    st.subheader("Tabel Data Pengguna Sepeda per Musim (Session)")
    season_user_count_df = season_user_count.reset_index()
    season_user_count_df.columns = ["Musim", "Jumlah Pengguna"]
    st.dataframe(season_user_count_df)

    st.subheader("Penjelasan")
    st.markdown("""
        Berdasarkan data penggunaan sepeda di tahun 2011 sampai dengan 2012, dibagi menjadi 4 musim, yaitu Musim Semi, Musim Panas,
        Musim Gugur, dan Musim Dingin. Dari 4 musim tersebut, musim yang memiliki penggunaan sepeda paling banyak berada pada musim 
        gugur dan musim yang memiliki pengguna sepeda paling sedikit berada pada musim semi.
    """)

with col4:
    # Membuat Pie Chart
    st.subheader("Visualisasi Pie Chart")
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'yellow']
    ax.pie(
        season_user_count,
        labels=season_user_count.index,
        autopct='%1.1f%%',
        colors=colors
    )
    ax.set_title("Jumlah Pengguna Berdasarkan 4 Musim Dataset")
    st.pyplot(fig)

st.header("Tren Penggunaan Sepeda")

col5, col6 = st.columns(2)
with col5:
    # Analisis Cuaca Tidak Stabil

    unstable_weather_df = df[df['weathersit'].isin(["Mendung", "Hujan", "Badai"])]

    monthly_trend = unstable_weather_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
    monthly_trend['tanggal'] = pd.to_datetime(monthly_trend['yr'].astype(str) + '-' + monthly_trend['mnth'].astype(str) + '-01')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_trend['tanggal'], monthly_trend['cnt'], marker='o', linestyle='-', label='Jumlah Peminjaman', color='blue')
    ax.set_title('Tren Penggunaan Sepeda saat Cuaca Tidak Stabil (2011-2012)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Penjelasan")
    st.markdown("""
        Berdasarkan track record data dibeberapa bulan, pengguna sepeda di tahun 2011 sampai dengan 2012 berjalan secara fluktuatif 
        karena dibeberapa bulan tersebut memiliki cuaca yang tidak stabil, akibatnya jumlah peminjaman dibeberapa bulan tersebut tidak 
        berjalan secara konstan.
    """)

with col6:
    # Mengconvert Tipe ke Datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    recent_months_df = df[df['dteday'] >= pd.Timestamp("2012-07-01")]

    monthly_usage = recent_months_df.groupby(recent_months_df['dteday'].dt.month)['cnt'].sum()
    month_mapping = {7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
    monthly_usage.index = monthly_usage.index.map(month_mapping)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_usage.index, monthly_usage.values, marker='o', linestyle='-', color='blue', label='Jumlah Penyewaan')

    # Labeling
    ax.set_title('Tren Penggunaan Sepeda (6 Bulan Terakhir)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.set_xticks(range(len(monthly_usage.index)))
    ax.set_xticklabels(monthly_usage.index, rotation=30)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Anotasi setiap titik
    for idx, value in enumerate(monthly_usage.values):
        ax.text(idx, value, f'{value}', fontsize=9, ha='center', va='bottom')

    st.pyplot(fig)

    st.subheader("Penjelasan")
    st.markdown("""
        Berdasarkan data di bulan Juli, Agustus, September, Oktober, November, dan Desember terakhir, pengguna sepeda di tahun 
        2012 berjalan secara stabil dan meningkat. Dari sini dapat dilihat bahwa pada bulan-bulan tersebut, jumlah peminjaman sepeda 
        berjalan secara konstan dan terus dan terus menurun.
    """)