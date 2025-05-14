    import dash
    from dash import dcc
    from dash import html
    import plotly.express as px
    import pandas as pd

    # Asumsi data day_df dan hour_df sudah tersedia dalam format CSV
    # Anda perlu memastikan file CSV ini ada di direktori yang sama atau menyediakan path lengkap

    try:
        day_df = pd.read_csv("day_cleaned.csv") # Ganti dengan nama file CSV data day yang sudah bersih
        hour_df = pd.read_csv("hour_cleaned.csv") # Ganti dengan nama file CSV data hour yang sudah bersih
    except FileNotFoundError:
        print("Pastikan file day_cleaned.csv dan hour_cleaned.csv ada di direktori yang sama.")
        print("Jika belum, Anda perlu menyimpan dataframe day_df dan hour_df yang sudah dibersihkan ke format CSV.")
        # Contoh menyimpan dataframes (jika Anda menjalankan ini setelah notebook Colab)
        # day_df.to_csv("day_cleaned.csv", index=False)
        # hour_df.to_csv("hour_cleaned.csv", index=False)
        exit() # Keluar jika file tidak ditemukan


    # --- Persiapan Data untuk Grafik ---

    # Grafik 1: Penggunaan Sepeda per Jam
    hour_usage = hour_df.groupby('hr')['count_cr'].sum().reset_index()
    fig_hourly_usage = px.line(hour_usage, x='hr', y='count_cr', title='Penggunaan Sepeda per Jam')

    # Grafik 2: Total Penyewaan Sepeda Berdasarkan Musim
    seasonal_usage = day_df.groupby('season')['count_cr'].sum().reset_index()
    fig_seasonal_usage = px.bar(seasonal_usage, x='season', y='count_cr', title='Total Penyewaan Sepeda Berdasarkan Musim')

    # Grafik 3: Pengguna Terdaftar vs Sementara per Bulan
    monthly_usage = day_df.groupby('month')[['registered', 'casual']].sum().reset_index()
    # Mengubah format data untuk Plotly agar bisa digabungkan dalam satu grafik
    monthly_usage_melted = monthly_usage.melt(id_vars='month', var_name='User Type', value_name='Count')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_usage_melted['month'] = pd.Categorical(monthly_usage_melted['month'], categories=month_order, ordered=True)
    monthly_usage_melted = monthly_usage_melted.sort_values('month')

    fig_monthly_users = px.bar(monthly_usage_melted, x='month', y='Count', color='User Type',
                               barmode='group', title='Pengguna Terdaftar vs Sementara per Bulan')

    # Grafik 4: Distribusi Pengguna Terdaftar dan Sementara (Pie Chart)
    total_registered = day_df['registered'].sum()
    total_casual = day_df['casual'].sum()
    user_distribution = pd.DataFrame({'Category': ['Terdaftar', 'Sementara'], 'Count': [total_registered, total_casual]})
    fig_user_distribution = px.pie(user_distribution, values='Count', names='Category', title='Distribusi Pengguna Terdaftar dan Sementara')


    # --- Inisialisasi Aplikasi Dash ---
    app = dash.Dash(__name__)

    # --- Layout Dashboard ---
    app.layout = html.Div(children=[
        html.H1(children='Dashboard Analisis Penggunaan Sepeda', style={'textAlign': 'center'}),

        html.Div(children='''
            Analisis pola penggunaan sepeda berdasarkan waktu, musim, dan jenis pengguna.
        ''', style={'textAlign': 'center'}),

        html.Div(className='row', children=[
            html.Div(children=[
                dcc.Graph(
                    id='hourly-usage-graph',
                    figure=fig_hourly_usage
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div(children=[
                dcc.Graph(
                    id='seasonal-usage-graph',
                    figure=fig_seasonal_usage
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

         html.Div(className='row', children=[
            html.Div(children=[
                dcc.Graph(
                    id='monthly-users-graph',
                    figure=fig_monthly_users
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

             html.Div(children=[
                dcc.Graph(
                    id='user-distribution-graph',
                    figure=fig_user_distribution
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

    ])

    # --- Menjalankan Server Dash ---
    if __name__ == '__main__':
        app.run_server(debug=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page title and icon (optional)
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon=":bike:")

# --- Load Data ---
# You'll need to have your 'all_data.csv' file accessible.
# If you are running this locally, make sure the CSV is in the same directory
# or provide the correct path.
# If you are deploying this, you might need to consider how to host your data.
try:
    df = pd.read_csv('all_data.csv')
except FileNotFoundError:
    st.error("Error: 'all_data.csv' not found. Please make sure the file is in the correct directory.")
    st.stop() # Stop the app if the file is not found

# --- Title and Introduction ---
st.title("Analisis Data Bike Sharing")
st.markdown("Dashboard ini menyajikan analisis data penggunaan sepeda sharing.")

# --- Data Overview ---
st.header("Gambaran Umum Data")
st.write("Data yang digunakan untuk analisis ini:")
st.dataframe(df.head()) # Display the first few rows of the dataframe

# --- Business Questions and Insights ---
st.header("Pertanyaan Bisnis dan Analisis")

st.subheader("1. Bagaimana tren musiman penggunaan sepeda memengaruhi berdasarkan pola waktu (harian, mingguan, atau bulanan)?")
st.write("""
Analisis penggunaan sepeda berdasarkan waktu menunjukkan beberapa pola yang signifikan:

- **Penggunaan Harian:** Hari-hari tertentu, seperti akhir pekan, sering kali menunjukkan lonjakan penggunaan. Ini mungkin disebabkan oleh aktivitas rekreasi atau kebijakan kerja dari rumah pada hari kerja.
- **Penggunaan Mingguan:** Pada tingkat mingguan, penggunaan sepeda cenderung meningkat pada akhir pekan dibandingkan dengan hari kerja.
- **Penggunaan Bulanan:** Analisis bulanan menunjukkan pola musiman yang jelas. Bulan-bulan tertentu, terutama musim panas, menunjukkan peningkatan signifikan dalam sewa sepeda.
""")

# Visualization for Seasonal Trend
st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")
seasonal_usage = df.groupby('season')['count_cr'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='count_cr', data=seasonal_usage)
plt.title('Total Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan')
st.pyplot(plt) # Display the plot in Streamlit
plt.clf() # Clear the plot figure after displaying

st.subheader("2. Apa perbedaan perilaku antara pengguna terdaftar dan pengguna sementara?")
st.write("""
Analisis perilaku pengguna berdasarkan kategori terdaftar dan sementara mengungkapkan beberapa perbedaan penting:

- **Karakteristik Pengguna:** Pengguna terdaftar cenderung menggunakan sepeda secara lebih konsisten, sementara pengguna sementara biasanya menggunakan layanan untuk keperluan jangka pendek.
- **Frekuensi Penggunaan:** Pengguna terdaftar memiliki frekuensi sewa yang lebih tinggi.
- **Respon terhadap Promosi:** Pengguna sementara mungkin lebih responsif terhadap promosi, sementara pengguna terdaftar lebih tertarik pada program loyalitas.
""")

# Visualization for User Type Distribution
st.subheader("Distribusi Pengguna Terdaftar dan Sementara")
total_registered = df['registered'].sum()
total_casual = df['casual'].sum()
labels = ['Terdaftar', 'Sementara']
sizes = [total_registered, total_casual]
colors = ['#ff9999','#66b3da']
fig1, ax1 = plt.subplots(figsize=(8, 8))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
ax1.axis('equal')
st.pyplot(fig1) # Display the pie chart in Streamlit
plt.clf() # Clear the plot figure after displaying


# --- Additional Visualizations (Example: Hourly Usage) ---
st.header("Analisis Penggunaan per Jam")
st.write("Visualisasi penggunaan sepeda berdasarkan jam dalam sehari.")
hourly_usage = df.groupby("hr").count_cr.sum().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly_usage, x='hr', y='count_cr', marker='o', color='b')
plt.title('Penggunaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Pengguna')
plt.grid(True)
st.pyplot(plt)
plt.clf()


# --- Conclusion ---
st.header("Kesimpulan")
st.write("""
- **Kesimpulan pertanyaan 1:** Tren penggunaan sepeda sangat dipengaruhi oleh pola waktu, dengan lonjakan penggunaan pada akhir pekan dan selama bulan-bulan musim panas.
- **Kesimpulan pertanyaan 2:** Pengguna terdaftar dan sementara menunjukkan perilaku yang berbeda dalam hal frekuensi dan tujuan penggunaan, yang penting untuk strategi pemasaran yang efektif.
""")

# --- How to Run ---
st.sidebar.header("Cara Menjalankan Dashboard Ini")
st.sidebar.markdown("""
1.  Simpan kode di atas sebagai file Python (`.py`), misalnya `dashboard_app.py`.
2.  Pastikan Anda memiliki file `all_data.csv` di direktori yang sama.
3.  Buka terminal atau command prompt.
4.  Instal Streamlit jika belum: `pip install streamlit pandas matplotlib seaborn`
5.  Jalankan aplikasi: `streamlit run dashboard_app.py`
""")
