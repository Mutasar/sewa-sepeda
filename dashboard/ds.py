import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/hour_dfrev5.csv", parse_dates=['date'])
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")

# Filter tanggal
date_range = st.sidebar.date_input("Pilih rentang tanggal", [df.date.min(), df.date.max()])

# Filter musim
seasons = df['season'].unique()
season_filter = st.sidebar.multiselect("Pilih musim:", seasons, default=seasons)

# Filter jam
hour_range = st.sidebar.slider("Pilih rentang jam:", 0, 23, (0, 23))

# Filter hari libur
holiday_option = st.sidebar.radio("Hari libur?", ["Semua", "Hanya Hari Libur", "Hanya Hari Biasa"])

# Filter cuaca
weather_filter = st.sidebar.multiselect("Pilih kondisi cuaca:", df['weather'].unique(), default=df['weather'].unique())

# Terapkan filter
filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['season'].isin(season_filter)) &
    (df['hr'] >= hour_range[0]) & (df['hr'] <= hour_range[1]) &
    (df['weather'].isin(weather_filter))
]

if holiday_option == "Hanya Hari Libur":
    filtered_df = filtered_df[filtered_df['holiday'] == 1]
elif holiday_option == "Hanya Hari Biasa":
    filtered_df = filtered_df[filtered_df['holiday'] == 0]

# Judul
st.title("🚲 Dashboard Bike Sharing")
st.markdown("Visualisasi ini menjawab dua pertanyaan utama terkait tren musiman dan perbedaan pengguna.")

# =======================
# Pertanyaan 1: Tren Musiman
# =======================
st.subheader(" Pertanyaan 1. bagaimana tren musiman penggunaan sepeda mempengaruhi berdasarkan pola waktu")

col1, col2 = st.columns(2)

# Lineplot: Tren per musim
st.markdown("** Total Sewa Sepeda per Jam (Rata-rata)**")
hourly_rentals = filtered_df.groupby('hr')['total_rentals'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=hourly_rentals, x='hr', y='total_rentals', palette='viridis', ax=ax2)
ax2.set_title("Rata-rata Total Sewa Sepeda per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Sewa")
st.pyplot(fig2)
    

# =======================
# Pertanyaan 2: Casual vs Registered
# =======================
st.subheader("👥 Pertanyaan 2. bagaimana perbedaan perilaku antara pengguna terdaftar dan pengguna sementara.")

# Bar chart per jam
st.markdown("**⏱️ Pola Waktu Pengguna: Casual vs Registered**")
hourly = filtered_df.groupby('hr')[['casual_users', 'registered_users']].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=hourly, x='hr', y='casual_users', label='Casual', ax=ax3)
sns.lineplot(data=hourly, x='hr', y='registered_users', label='Registered', ax=ax3)
ax3.set_title("Rata-rata Penggunaan per Jam")
st.pyplot(fig3)


# Footer
st.markdown("---")
st.markdown("mutasar @2025")
