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
