import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/bike_sharing.csv")

# Judul Dashboard
st.title("Dashboard Sewa Sepeda")

# Buat dua kolom: kiri untuk gambar, kanan untuk dashboard
col1, col2 = st.columns([1, 2])  # rasio kolom: 1 bagian kiri, 2 bagian kanan

# Kolom kiri: gambar
with col1:
 st.image("https://raw.githubusercontent.com/Mutasar/sewa-sepeda/main/sepeda.png", caption="Sewa sepeda", use_container_width=True)

# Kolom kanan: dashboard
with col2:
    st.title("Data hasil Analisa sewa sepeda ")

    st.subheader("Jumlah Penyewaan Sepeda per Hari")
    fig_daily = px.line(df, x='dteday', y='cnt', title='Jumlah Penyewaan Sepeda per Hari')
    st.plotly_chart(fig_daily)

    st.subheader("Pilih Musim")
    season = st.selectbox("Season", sorted(df['season'].unique()))

    filtered_df = df[df['season'] == season]

    st.subheader(f"Jumlah Penyewaan Sepeda pada Musim {season}")
    fig_season = px.bar(filtered_df, x='dteday', y='cnt', title=f'Jumlah Penyewaan Musim {season}')
    st.plotly_chart(fig_season)