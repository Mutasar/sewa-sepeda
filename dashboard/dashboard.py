import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Pastikan set_page_config adalah panggilan Streamlit pertama
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Pastikan kolom tanggal diubah menjadi tipe datetime
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
    return data

# Memuat data dari URL GitHub
try:
    # Ganti URL ini dengan URL file CSV Anda yang sebenarnya jika berbeda
    day_df = load_data('https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/day_df%20rev4.csv')
    hour_df = load_data('https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/hour_df%20rev4.csv')
except Exception as e:
    st.error(f"Gagal memuat data dari URL. Pastikan URL benar dan file tersedia. Error: {e}")
    st.stop() # Berhenti jika gagal memuat data

st.title("Dashboard Analisis Data Sewa Sepeda")

# --- Buat 2 Kolom ---
col1, col2 = st.columns(2)

# --- Konten untuk Kolom 1 (Analisis Tren Musiman) ---
with col1:
    st.header("Pertanyaan 1: tren musiman penggunaan sepeda memengaruhi berdasarkan pola waktu")

    # Visualisasi Tren Harian dari Waktu ke Waktu
    st.subheader("Tren Total Sewa bulanan")
    fig1, ax1 = plt.subplots(figsize=(10, 5)) # Sesuaikan ukuran untuk kolom
    sns.lineplot(x='date', y='total_rentals', data=day_df, ax=ax1)
    ax1.set_title('Tren Total Sewa Bulan')
    ax1.set_xlabel('bulan')
    ax1.set_ylabel('Jumlah Sewa')
    plt.xticks(rotation=45)
    plt.tight_layout() # Tambahkan tight_layout untuk penyesuaian
    st.pyplot(fig1)

    # Visualisasi Rata-rata Sewa Harian per Musim
    st.subheader("Rata-rata Sewa per Musim")
    avg_rentals_per_season = day_df.groupby('season')['total_rentals'].mean().reset_index()
    # Mengurutkan musim secara logis jika perlu (Spring, Summer, Fall, Winter)
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    avg_rentals_per_season['season'] = pd.Categorical(avg_rentals_per_season['season'], categories=season_order, ordered=True)
    avg_rentals_per_season = avg_rentals_per_season.sort_values('season')

    fig2, ax2 = plt.subplots(figsize=(8, 4)) # Sesuaikan ukuran
    sns.barplot(x='season', y='total_rentals', data=avg_rentals_per_season, ax=ax2, palette='viridis')
    ax2.set_title('Rata-rata Sewa Harian per Musim')
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Rata-rata Jumlah Sewa')
    plt.tight_layout()
    st.pyplot(fig2)

    # Opsional: Visualisasi Dekomposisi Tren Musiman Tahunan
    st.subheader("Dekomposisi Tren Tahunan")
    day_df_ts = day_df.set_index('date').sort_index()
    try:
        result = seasonal_decompose(day_df_ts['total_rentals'], model='additive', period=365)
        fig_decomp = result.plot()
        fig_decomp.set_size_inches(10, 6) # Sesuaikan ukuran
        plt.tight_layout()
        st.pyplot(fig_decomp)
    except Exception as e:
        st.warning(f"Tidak dapat menampilkan dekomposisi musiman. Pastikan data memiliki periode yang cukup. Error: {e}")


# --- Konten untuk Kolom 2 (Analisis Perilaku Pengguna) ---
with col2:
    st.header("Pertanyaan 2: perbedaan perilaku antara pengguna terdaftar dan pengguna sementara.")

    # Menggabungkan data casual dan registered
    day_df_users = day_df.melt(id_vars=['date', 'season', 'month', 'year', 'weekday'],
                               value_vars=['casual_users', 'registered_users'],
                               var_name='user_type',
                               value_name='rental_count')

    hour_df_users = hour_df.melt(id_vars=['date', 'season', 'month', 'year', 'weekday', 'hr'],
                               value_vars=['casual_users', 'registered_users'],
                               var_name='user_type',
                               value_name='rental_count')

    # Visualisasi Perbandingan Sewa Berdasarkan Jam
    st.subheader("Sewa per Jam (Kasual vs Terdaftar)")
    fig3, ax3 = plt.subplots(figsize=(10, 5)) # Sesuaikan ukuran
    sns.lineplot(x='hr', y='rental_count', hue='user_type', data=hour_df_users, ax=ax3)
    ax3.set_title('Perbandingan Sewa Berdasarkan Jam')
    ax3.set_xlabel('Jam')
    ax3.set_ylabel('Jumlah Sewa')
    ax3.set_xticks(range(0, 24, 2)) # Tampilkan setiap 2 jam untuk kerapian
    ax3.grid(axis='x')
    ax3.legend(title='Tipe Pengguna')
    plt.tight_layout()
    st.pyplot(fig3)

    # Visualisasi Perbandingan Sewa Berdasarkan Hari dalam Seminggu
    st.subheader("Sewa per Hari (Kasual vs Terdaftar)")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    rentals_by_weekday_usertype = day_df_users.groupby(['weekday', 'user_type'])['rental_count'].sum().reset_index()
    rentals_by_weekday_usertype['weekday'] = pd.Categorical(rentals_by_weekday_usertype['weekday'], categories=weekday_order, ordered=True)
    rentals_by_weekday_usertype = rentals_by_weekday_usertype.sort_values('weekday')

    fig4, ax4 = plt.subplots(figsize=(10, 5)) # Sesuaikan ukuran
    sns.barplot(x='weekday', y='rental_count', hue='user_type', data=rentals_by_weekday_usertype, palette='plasma', ax=ax4)
    ax4.set_title('Total Sewa Berdasarkan Hari')
    ax4.set_xlabel('Hari dalam Seminggu')
    ax4.set_ylabel('Total Jumlah Sewa')
    ax4.legend(title='Tipe Pengguna')
    ax4.grid(axis='y', linestyle='--')
    plt.xticks(rotation=45) # Rotasi label x agar tidak bertumpuk
    plt.tight_layout()
    st.pyplot(fig4)

    # Ringkasan Statistik Pengguna
    st.subheader("Total Sewa per Tipe Pengguna")
    user_summary = day_df[['casual_users', 'registered_users', 'total_rentals']].sum().reset_index()
    user_summary.columns = ['User Type', 'Total Rentals']
    user_summary['User Type'] = user_summary['User Type'].replace({
        'casual_users': 'Pengguna Kasual',
        'registered_users': 'Pengguna Terdaftar',
        'total_rentals': 'Total Semua Pengguna'
    })
    st.dataframe(user_summary)


# --- Bagian Kesimpulan (di bawah kolom) ---
st.header("Kesimpulan")
st.write("""
Berdasarkan visualisasi di atas, dapat disimpulkan beberapa hal:

**Tren Musiman:** Layanan sewa sepeda menunjukkan pola penggunaan yang sangat dipengaruhi oleh musim, dengan puncak di musim gugur dan panas. Hari akhir pekan juga menunjukkan penggunaan yang lebih tinggi.

**Perilaku Pengguna:** Pengguna terdaftar adalah basis pelanggan utama dengan volume sewa yang jauh lebih tinggi. Pola penggunaan harian (jam) dan mingguan (hari) sangat berbeda antara pengguna kasual (lebih ke rekreasi, puncak tengah hari/akhir pekan) dan terdaftar (lebih ke komuter, puncak pagi/sore di hari kerja).

Insight ini sangat penting untuk strategi operasional, pemasaran, dan perencanaan sumber daya untuk layanan sewa sepeda.
""")
