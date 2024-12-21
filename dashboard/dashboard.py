import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Dashboard Analisis Bike Sharing")

# Mengambil Data
day_df = pd.read_csv("day.csv", delimiter=",")
hour_df = pd.read_csv("hour.csv", delimiter=",")

# Mapping Season
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
day_df['season'] = day_df['season'].map(season_mapping)
hour_df['season'] = hour_df['season'].map(season_mapping)

# Mapping Month
month_mapping = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
day_df['mnth'] = day_df['mnth'].map(month_mapping)
hour_df['mnth'] = hour_df['mnth'].map(month_mapping)

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

# Sidebar untuk memilih dataset
dataset_option = st.sidebar.selectbox("Pilih Dataset:", ["Day", "Hour", "Other"])
if dataset_option == "Day":
    st.subheader("Dataset day.csv")
    df = day_df
elif dataset_option == "Hour":
    st.subheader("Dataset hour.csv")
    df = hour_df
else:
    st.subheader("")

if dataset_option == "Day":
    # Menampilkan seluruh data dari day_df dan hour_df
    st.dataframe(hour_df, width=1000, height=500)
    day_df.rename(columns={'instant': 'id_pengguna'}, inplace=True)


    st.header("Explorasi Data")
    st.subheader("Persentase Jumlah Pengguna Berdasarkan :")
    tab1, tab2, tab3 = st.tabs(['Bulan', 'Registered', 'Cuaca'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Bulan')
            data = {
                'mnth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'cnt': [134933, 151352, 228920, 269094, 331686, 344948, 346342, 351194, 345991, 322352, 254831, 211036]
            }
            day_month_table = pd.DataFrame(data)

             # Hitung total jumlah pengguna per bulan
            monthly_data = day_month_table.groupby('mnth').agg({
                'cnt': 'sum'
            }).reset_index()

            # Hitung persentase pengguna
            total_cnt = monthly_data['cnt'].sum()
            monthly_data['Persentase Pengguna'] = (monthly_data['cnt'] / total_cnt) * 100

            # Tambahkan kolom nama bulan
            monthly_data['Bulan'] = monthly_data['mnth'].map({
                1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
                7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
            })

            # Urutkan berdasarkan kolom 'mnth' untuk memastikan bulan terurut
            monthly_data = monthly_data.sort_values('mnth')

            # Atur ulang urutan kolom
            monthly_data = monthly_data[['Bulan', 'cnt', 'Persentase Pengguna']]

            # Format nilai jumlah pengguna dan persentase
            monthly_data['cnt'] = monthly_data['cnt'].astype(int)
            monthly_data['Persentase Pengguna'] = monthly_data['Persentase Pengguna'].apply(lambda x: f"{x:.2f}%")

            # Tampilkan di Streamlit
            st.dataframe(monthly_data)

        with col2:
            st.subheader("Penjelasan")
            st.markdown("""
                Jumlah pengguna sepeda berdasarkan tiap bulannya berjalan fluktiatif artinya nilai dapat meningkat dan menurun. Seperti pada tabel tersebut, Pada bulan Januari sampai Agustus jumlah pengguna sepeda cenderung meningkat yang ditandai dengan persentase yang terus naik namun mulai Agustus sampai dengan Desember jumlah pengguna sepeda cenderung turun. Dari informasi tersebut kita mendapatkan insight baru tentang perkembangan jumlah pengguna sepeda di setiap bulannya.
            """)

    with tab2:
        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Registed')
            # Dataframe awal (simulasikan 'day_df')
            monthly_data = day_df.groupby('mnth').agg({
                'cnt': 'sum',
                'registered': 'sum'
            }).reset_index()

            # Hitung persentase registrasi
            monthly_data['Persentase Registrasi'] = (monthly_data['registered'] / monthly_data['cnt']) * 100

            # Format angka dan persentase
            monthly_data['cnt'] = monthly_data['cnt'].apply(lambda x: f"{x:,.0f}")
            monthly_data['registered'] = monthly_data['registered'].apply(lambda x: f"{x:,.0f}")
            monthly_data['Persentase Registrasi'] = monthly_data['Persentase Registrasi'].apply(lambda x: f"{x:.2f}%")

            # Tampilkan tabel di Streamlit
            st.dataframe(monthly_data)

        with col4:
            st.subheader('Penjelasan')
            st.markdown("""
                Jumlah pengguna sepeda berdasarkan jumlah register tiap bulannya berjalan secara fluktuatif yang artinya hanya dibeberapa bulan saja yang terdapat jumlah pengguna yang banyak. Seperti pada tabel tersebut, Pada bulan Januari sampai dengan Juli jumlah pengguna sepeda yang registrasi cenderung menurun. Sedangkan pada bulan Juli sampai dengan Desember jumlah pengguna sepeda yang registrasi cenderung meningkat.Dari informasi tersbut kita mendapatkan insight baru tentang perkembangan jumlah pengguna sepeda yang registrasi tiap bulannya.
            """)

    with tab3 :
        col5, col6 = st.columns(2)
        with col5:
            # Membuat tabel analisis jumlah pengguna berdasarkan cuaca
            weather_user_count_day = day_df.groupby('weathersit')['cnt'].sum()

            # Menghitung persentase pengguna berdasarkan cuaca
            total_users = weather_user_count_day.sum()
            weather_user_percentage = (weather_user_count_day / total_users) * 100

            weather_user_df = pd.DataFrame({
                'Kondisi Cuaca': weather_user_count_day.index,
                'Jumlah Pengguna': weather_user_count_day.values,
                'Persentase Pengguna (%)': weather_user_percentage.values
            })

            st.dataframe(
                weather_user_df.style.format({
                    'Jumlah Pengguna': '{:,.0f}',
                    'Persentase Pengguna (%)': '{:.2f}'
                })
            )
        
        with col6:
            st.subheader('Penjelasan')
            st.markdown("""
                Analisis ini menampilkan jumlah pengguna sepeda berdasarkan kondisi cuaca yang terjadi pada hari tersebut. Dari tabel tersebut, dapat dilihat bahwa
                terdapat penggunaan sepeda di hari yang cuacanya paling sering terjadi adalah Musim Panas. Persebaran persentase penggunaan sepeda
                di setiap kondisi cuaca menunjukkan bahwa hari yang cuaca Musim Panas memiliki persentase penggunaan sepeda yang tinggi, sekitar 69%.
            """)

    st.header('Visualisasi Data')
    col7, col8 = st.columns(2)
    with col7:
        st.subheader("Pie Chart Jumlah Penggunaan Sepeda Berdasarkan Musim")
        # Tabel Analisis Data
        season_user_count = day_df.groupby('season')['cnt'].sum()

        # Menampilkan Data
        season_user_count_df = season_user_count.reset_index()
        season_user_count_df.columns = ["Musim", "Jumlah Pengguna"]

        # Membuat Pie Chart
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
        
        with st.expander("Penjelasan"):
            st.dataframe(season_user_count_df)

            st.subheader("Penjelasan")
            st.markdown("""
                Berdasarkan data penggunaan sepeda di tahun 2011 sampai dengan 2012, dibagi menjadi 4 musim, yaitu Musim Semi, Musim Panas,
                Musim Gugur, dan Musim Dingin. Dari 4 musim tersebut, musim yang memiliki penggunaan sepeda paling banyak berada pada musim 
                gugur dan musim yang memiliki pengguna sepeda paling sedikit berada pada musim semi.
            """)

    with col8:
        st.subheader("Bar Chart Jumlah Penggunaan Sepeda Berdasarkan Cuaca")
        # Analisis Cuaca Tidak Stabil
        # Mengelompokkan data berdasarkan kondisi cuaca
        weather_trend = day_df.groupby('weathersit')['cnt'].sum().reset_index()
        weather_trend = weather_trend.rename(columns={'cnt': 'Jumlah Pengguna'})

        # Membuat Bar Chart
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(weather_trend['weathersit'], weather_trend['Jumlah Pengguna'], color=['skyblue', 'green', 'lightcoral'])
        ax.set_title('Penggunaan Sepeda Saat Cuaca Tidak Stabil', fontsize=14)
        ax.set_xlabel('Kondisi Cuaca', fontsize=12)
        ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Menampilkan Bar Chart di Streamlit
        st.pyplot(fig)

        with st.expander("Penjelasan"):
            # Menampilkan Tabel Data
            st.subheader("Tabel Data Penggunaan Sepeda")
            st.table(weather_trend)

            st.subheader("Penjelasan")
            st.markdown("""
                Berdasarkan track record data dibeberapa bulan, pengguna sepeda di tahun 2011 sampai dengan 2012 berjalan cukup stabil
                karena dibeberapa bulan tersebut memiliki cuaca yang cenderung cerah, akibatnya jumlah peminjaman dibeberapa bulan tersebut dapat
                berjalan secara konstan.
            """)

    col9, col10 = st.columns(2)
    with col9:
        st.subheader("Line Chart Jumlah Penggunaan Sepeda Di 6 Bulan Terakhir")
        # Mengconvert Tipe ke Datetime
        df['dteday'] = pd.to_datetime(day_df['dteday'])
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

        with st.expander('Penjelasan'):
            st.markdown("""
                    Berdasarkan data di bulan Juli, Agustus, September, Oktober, November, dan Desember terakhir, pengguna sepeda di tahun 
                    2012 berjalan secara stabil dan meningkat. Dari sini dapat dilihat bahwa pada bulan-bulan tersebut, jumlah peminjaman sepeda 
                    berjalan secara konstan dan terus dan terus menurun.
            """)
    
    st.header("Kesimpulan Data")
    col11, col12 = st.columns(2)
    with col11:
        st.subheader("Explore Data")
        st.markdown("""
            Pada tahap ini, Kita mendapatkan insight baru berupa persentase dari jumlah penggunaan sepeda berdasarkan beberapa kriteria. Dari adanya tabel informasi tersebut, kita jadi bisa melihat pola-pola jumlah pengguna sepeda di tahun 2011 sampai dengan 2012.
        """)

    with col12:
        st.subheader("Visualisasi Data")
        st.markdown("""
            Pada tahap ini, kita diberikan visualisasi data, baik berupa pie chart, bar chart, line chart yang representasikan jumlah pengguna berdasarkan beberapa kriteria. Dari adanya tabel informasi tersebut, kita jadi bisa melihat frekuensi-frekuensi datanya.
        """)

elif dataset_option == "Hour":
    st.subheader("Dataset hour.csv")
    df = hour_df

    st.dataframe(hour_df, width=1000, height=500)
    hour_df.rename(columns={'instant': 'id_pengguna'}, inplace=True)

    st.header("Explorasi Data")
    st.subheader("Persentase Jumlah Pengguna Berdasarkan :")
    tab4, tab5, tab6 = st.tabs(['Bulan', 'Registered', 'Cuaca'])
    with tab4:
        col13, col14 = st.columns(2)
        with col13:
            st.subheader('Bulan')
            data = {
                'mnth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'cnt': [134933, 151352, 228920, 269094, 331686, 344948, 346342, 351194, 345991, 322352, 254831, 211036]
            }

            hour_month_table = pd.DataFrame(data)
            monthly_data = hour_month_table.groupby('mnth').agg({
                'cnt': 'sum'
            }).reset_index()

            total_cnt = monthly_data['cnt'].sum()
            monthly_data['Persentase Pengguna'] = (monthly_data['cnt'] / total_cnt) * 100
            monthly_data['Bulan'] = monthly_data['mnth'].map({
                1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
                7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
            })

            monthly_data = monthly_data.sort_values('mnth')
            monthly_data = monthly_data[['Bulan', 'cnt', 'Persentase Pengguna']]
            monthly_data['cnt'] = monthly_data['cnt'].astype(int)
            monthly_data['Persentase Pengguna'] = monthly_data['Persentase Pengguna'].apply(lambda x: f"{x:.2f}%")

            st.dataframe(monthly_data)

        with col14:
            st.subheader("Penjelasan")
            st.markdown("""
                Jumlah pengguna sepeda berdasarkan tiap bulannya berjalan fluktiatif artinya nilai dapat meningkat dan menurun. Seperti pada tabel tersebut, Pada bulan Januari sampai Agustus jumlah pengguna sepeda cenderung meningkat yang ditandai dengan persentase yang terus naik namun mulai Agustus sampai dengan Desember jumlah pengguna sepeda cenderung turun. Dari informasi tersebut kita mendapatkan insight baru tentang perkembangan jumlah pengguna sepeda di setiap bulannya.
            """)

    with tab5:
        col15, col16 = st.columns(2)
        with col15:
            st.subheader('Registed')
            monthly_data = hour_df.groupby('mnth').agg({
                'cnt': 'sum',
                'registered': 'sum'
            }).reset_index()

            monthly_data['Persentase Registrasi'] = (monthly_data['registered'] / monthly_data['cnt']) * 100
            monthly_data['cnt'] = monthly_data['cnt'].apply(lambda x: f"{x:,.0f}")
            monthly_data['registered'] = monthly_data['registered'].apply(lambda x: f"{x:,.0f}")
            monthly_data['Persentase Registrasi'] = monthly_data['Persentase Registrasi'].apply(lambda x: f"{x:.2f}%")

            st.dataframe(monthly_data)

        with col16:
            st.subheader('Penjelasan')
            st.markdown("""
                Jumlah pengguna sepeda berdasarkan jumlah register tiap bulannya berjalan secara fluktuatif yang artinya hanya dibeberapa bulan saja yang terdapat jumlah pengguna yang banyak. Seperti pada tabel tersebut, Pada bulan Januari sampai dengan Juli jumlah pengguna sepeda yang registrasi cenderung menurun. Sedangkan pada bulan Juli sampai dengan Desember jumlah pengguna sepeda yang registrasi cenderung meningkat.Dari informasi tersbut kita mendapatkan insight baru tentang perkembangan jumlah pengguna sepeda yang registrasi tiap bulannya.
            """)

    with tab6 :
        col17, col18 = st.columns(2)
        with col17:
            # Membuat tabel analisis jumlah pengguna berdasarkan cuaca
            weather_user_count_hour = hour_df.groupby('weathersit')['cnt'].sum()
            total_users = weather_user_count_hour.sum()
            weather_user_percentage = (weather_user_count_hour / total_users) * 100

            weather_user_df = pd.DataFrame({
                'Kondisi Cuaca': weather_user_count_hour.index,
                'Jumlah Pengguna': weather_user_count_hour.values,
                'Persentase Pengguna (%)': weather_user_percentage.values
            })

            st.dataframe(
                weather_user_df.style.format({
                    'Jumlah Pengguna': '{:,.0f}',
                    'Persentase Pengguna (%)': '{:.2f}'
                })
            )
        
        with col18:
            st.subheader('Penjelasan')
            st.markdown("""
                Analisis ini menampilkan jumlah pengguna sepeda berdasarkan kondisi cuaca yang terjadi pada hari tersebut. Dari tabel tersebut, dapat dilihat bahwa
                terdapat penggunaan sepeda di hari yang cuacanya paling sering terjadi adalah Musim Panas. Persebaran persentase penggunaan sepeda
                di setiap kondisi cuaca menunjukkan bahwa hari yang cuaca Musim Panas memiliki persentase penggunaan sepeda yang tinggi, sekitar 69%.
            """)



    st.header('Visualisasi Data')
    col19, col20 = st.columns(2)
    with col19:
        st.subheader("Pie Chart Jumlah Penggunaan Sepeda Berdasarkan Musim")

        season_user_count = hour_df.groupby('season')['cnt'].sum()
        season_user_count_df = season_user_count.reset_index()
        season_user_count_df.columns = ["Musim", "Jumlah Pengguna"]

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
        
        with st.expander("Penjelasan"):
            st.dataframe(season_user_count_df)

            st.subheader("Penjelasan")
            st.markdown("""
                Berdasarkan data penggunaan sepeda di tahun 2011 sampai dengan 2012, dibagi menjadi 4 musim, yaitu Musim Semi, Musim Panas,
                Musim Gugur, dan Musim Dingin. Dari 4 musim tersebut, musim yang memiliki penggunaan sepeda paling banyak berada pada musim 
                gugur dan musim yang memiliki pengguna sepeda paling sedikit berada pada musim semi.
            """)

    with col20:
        st.subheader("Bar Chart Jumlah Penggunaan Sepeda Berdasarkan Cuaca")

        weather_trend = hour_df.groupby('weathersit')['cnt'].sum().reset_index()
        weather_trend = weather_trend.rename(columns={'cnt': 'Jumlah Pengguna'})

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(weather_trend['weathersit'], weather_trend['Jumlah Pengguna'], color=['skyblue', 'green', 'lightcoral'])
        ax.set_title('Penggunaan Sepeda Saat Cuaca Tidak Stabil', fontsize=14)
        ax.set_xlabel('Kondisi Cuaca', fontsize=12)
        ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)

        with st.expander("Penjelasan"):
            st.subheader("Tabel Data Penggunaan Sepeda")
            st.table(weather_trend)

            st.subheader("Penjelasan")
            st.markdown("""
                Berdasarkan track record data dibeberapa bulan, pengguna sepeda di tahun 2011 sampai dengan 2012 berjalan cukup stabil
                karena dibeberapa bulan tersebut memiliki cuaca yang cenderung cerah, akibatnya jumlah peminjaman dibeberapa bulan tersebut dapat
                berjalan secara konstan.
            """)

    col21, col22 = st.columns(2)
    with col21:
        st.subheader("Line Chart Jumlah Penggunaan Sepeda Di 6 Bulan Terakhir")
        df['dteday'] = pd.to_datetime(hour_df['dteday'])
        recent_months_df = df[df['dteday'] >= pd.Timestamp("2012-07-01")]

        monthly_usage = recent_months_df.groupby(recent_months_df['dteday'].dt.month)['cnt'].sum()
        month_mapping = {7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
        monthly_usage.index = monthly_usage.index.map(month_mapping)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(monthly_usage.index, monthly_usage.values, marker='o', linestyle='-', color='blue', label='Jumlah Penyewaan')

        ax.set_title('Tren Penggunaan Sepeda (6 Bulan Terakhir)')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Pengguna Sepeda')
        ax.set_xticks(range(len(monthly_usage.index)))
        ax.set_xticklabels(monthly_usage.index, rotation=30)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

        for idx, value in enumerate(monthly_usage.values):
            ax.text(idx, value, f'{value}', fontsize=9, ha='center', va='bottom')

        st.pyplot(fig)

        with st.expander('Penjelasan'):
            st.markdown("""
                    Berdasarkan data di bulan Juli, Agustus, September, Oktober, November, dan Desember terakhir, pengguna sepeda di tahun 
                    2012 berjalan secara stabil dan meningkat. Dari sini dapat dilihat bahwa pada bulan-bulan tersebut, jumlah peminjaman sepeda 
                    berjalan secara konstan dan terus dan terus menurun.
            """)
    
    st.header("Kesimpulan Data")
    col22, col23 = st.columns(2)
    with col22:
        st.subheader("Explore Data")
        st.markdown("""
            Pada tahap ini, Kita mendapatkan insight baru berupa persentase dari jumlah penggunaan sepeda berdasarkan beberapa kriteria. Dari adanya tabel informasi tersebut, kita jadi bisa melihat pola-pola jumlah pengguna sepeda di tahun 2011 sampai dengan 2012.
        """)

    with col23:
        st.subheader("Visualisasi Data")
        st.markdown("""
            Pada tahap ini, kita diberikan visualisasi data, baik berupa pie chart, bar chart, line chart yang representasikan jumlah pengguna berdasarkan beberapa kriteria. Dari adanya tabel informasi tersebut, kita jadi bisa melihat frekuensi-frekuensi datanya.
        """)

else:
    st.subheader("Data Tidak Ada")