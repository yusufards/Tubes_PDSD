import streamlit as st
import pandas as pd
import plotly.express as px
import os
print(os.getcwd())  # Cek direktori kerja saat ini

# Membaca file CSV dari direktori proyek
df = pd.read_csv("day.csv")

# Membuat Title
st.title("Bike Dashboard")

# Mengubah format tanggal menjadi datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Menambahkan kolom bulan, tahun, dan hari dalam seminggu
df['month'] = df['dteday'].dt.strftime("%B %Y")
df['year'] = df['dteday'].dt.year
df['day_of_week'] = df['dteday'].dt.day_name()

# Sidebar untuk memilih filter
st.sidebar.header("Filter Data")

# Filter berdasarkan tahun
selected_year = st.sidebar.selectbox("Pilih Tahun:", df['year'].unique())

# Filter data berdasarkan tahun yang dipilih
filtered_data = df[df['year'] == selected_year]

# Filter berdasarkan bulan
selected_month = st.sidebar.selectbox("Pilih Bulan:", filtered_data['month'].unique())

# Filter data berdasarkan bulan yang dipilih
filtered_data = filtered_data[filtered_data['month'] == selected_month]

# Filter berdasarkan kondisi cuaca
weather_conditions = {
    1: "Cerah",
    2: "Kabut/Berawan",
}
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", list(weather_conditions.values()))

# Mendapatkan kunci kondisi cuaca yang dipilih
weather_key = [k for k, v in weather_conditions.items() if v == selected_weather][0]

# Filter data berdasarkan kondisi cuaca yang dipilih
filtered_data = filtered_data[filtered_data['weathersit'] == weather_key]

# Menampilkan Line Chart
st.subheader(f"Tren Penyewaan Sepeda pada {selected_month} ({selected_year})")
st.line_chart(filtered_data.groupby('dteday')['cnt'].sum().reset_index().set_index('dteday'))

# Membuat tabs untuk tabel, pie chart, dan analisis tambahan
tab1, tab2, tab3 = st.tabs(['Table', 'Pie Chart', 'Analisis Tambahan'])

with tab1:
    st.subheader("Dataset Penyewaan Sepeda")
    st.dataframe(filtered_data)

with tab2:
    # Mengelompokkan data berdasarkan hari dalam seminggu dan menghitung total penyewaan
    rental_comparison = filtered_data.groupby('day_of_week')['cnt'].sum().reset_index()
    rental_comparison = rental_comparison.sort_values(by='cnt', ascending=False)
    
    # Membuat pie chart
    fig = px.pie(rental_comparison, values='cnt', names='day_of_week',
                 title='Perbandingan Penyewaan Sepeda Berdasarkan Hari',
                 height=400, width=400)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0))
    
    # Menampilkan pie chart
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Analisis Tambahan")
    
    # Analisis 1: Total Penyewaan Sepeda per Hari
    st.write("### Total Penyewaan Sepeda per Hari")
    daily_rentals = filtered_data.groupby('dteday')['cnt'].sum().reset_index()
    st.bar_chart(daily_rentals.set_index('dteday'))

    # Analisis 2: Rata-rata Penyewaan Sepeda per Hari dalam Seminggu
    st.write("### Rata-rata Penyewaan Sepeda per Hari dalam Seminggu")
    avg_rentals_by_day = filtered_data.groupby('day_of_week')['cnt'].mean().reset_index()
    st.bar_chart(avg_rentals_by_day.set_index('day_of_week'))

    # Analisis 3: Pengaruh Suhu terhadap Penyewaan Sepeda
    st.write("### Pengaruh Suhu terhadap Penyewaan Sepeda")
    fig_temp = px.scatter(filtered_data, x='temp', y='cnt', 
                          title='Pengaruh Suhu terhadap Penyewaan Sepeda',
                          labels={'temp': 'Suhu (Normalized)', 'cnt': 'Total Penyewaan'})
    st.plotly_chart(fig_temp, use_container_width=True)

    # Analisis 4: Pengaruh Kelembaban terhadap Penyewaan Sepeda
    st.write("### Pengaruh Kelembaban terhadap Penyewaan Sepeda")
    fig_hum = px.scatter(filtered_data, x='hum', y='cnt', 
                         title='Pengaruh Kelembaban terhadap Penyewaan Sepeda',
                         labels={'hum': 'Kelembaban (Normalized)', 'cnt': 'Total Penyewaan'})
    st.plotly_chart(fig_hum, use_container_width=True)

    # Analisis 5: Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda
    st.write("### Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
    fig_windspeed = px.scatter(filtered_data, x='windspeed', y='cnt', 
                               title='Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda',
                               labels={'windspeed': 'Kecepatan Angin (Normalized)', 'cnt': 'Total Penyewaan'})
    st.plotly_chart(fig_windspeed, use_container_width=True)