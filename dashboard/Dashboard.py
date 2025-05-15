
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Analisa Sewa Sepeda", layout="wide")

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/day%20clean.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Mutasar/sewa-sepeda/refs/heads/main/dashboard/hour%20clean.csv")

st.title("🚲 Dashboard Analisa Sewa Sepeda")

# Sidebar
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Select Year", options=day_df["year"].unique(), default=day_df["year"].unique())
selected_season = st.sidebar.multiselect("Select Season", options=day_df["season"].unique(), default=day_df["season"].unique())

# Filtered Data
filtered_day_df = day_df[(day_df["year"].isin(selected_year)) & (day_df["season"].isin(selected_season))]

# KPIs
total_rides = int(filtered_day_df["count_cr"].sum())
avg_daily_rides = int(filtered_day_df["count_cr"].mean())
total_registered = int(filtered_day_df["registered"].sum())
total_casual = int(filtered_day_df["casual"].sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rides", f"{total_rides:,}")
col2.metric("Avg Daily Rides", f"{avg_daily_rides:,}")
col3.metric("Registered Users", f"{total_registered:,}")
col4.metric("Casual Users", f"{total_casual:,}")

# Line Chart - Daily Trend
st.subheader("📈 Daily Ride Count")
fig1, ax1 = plt.subplots()
filtered_day_df["dteday"] = pd.to_datetime(filtered_day_df["dteday"])
filtered_day_df = filtered_day_df.sort_values("dteday")
sns.lineplot(data=filtered_day_df, x="dteday", y="count_cr", ax=ax1)
ax1.set_title("Total Rides Per Day")
ax1.set_xlabel("Date")
ax1.set_ylabel("Ride Count")
st.pyplot(fig1)

# Bar Chart - Average Hourly Rides
st.subheader("🕒 Average Hourly Ride Count")
avg_hourly = hour_df.groupby("hr")["count_cr"].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=avg_hourly, x="hr", y="count_cr", ax=ax2, palette="viridis")
ax2.set_title("Average Rides by Hour")
ax2.set_xlabel("Hour")
ax2.set_ylabel("Average Ride Count")
st.pyplot(fig2)

# Boxplot - Weather Situation
st.subheader("🌦 Ride Count by Weather Situation")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_day_df, x="weather_situation", y="count_cr", ax=ax3, palette="Set2")
ax3.set_title("Distribution of Rides by Weather")
ax3.set_xlabel("Weather Situation")
ax3.set_ylabel("Ride Count")
st.pyplot(fig3)

# Category Comparison
st.subheader("📊 Weekday vs Weekend")
cat_df = filtered_day_df.groupby("category_days")["count_cr"].mean().reset_index()
fig4, ax4 = plt.subplots()
sns.barplot(data=cat_df, x="category_days", y="count_cr", palette="coolwarm", ax=ax4)
ax4.set_title("Average Rides: Weekdays vs Weekends")
ax4.set_xlabel("Category")
ax4.set_ylabel("Average Ride Count")
st.pyplot(fig4)

st.subheader("🔍 Average Users by Hour (Registered vs Casual)")

avg_hour_group = hour_df.groupby("hr")[["registered", "casual"]].mean().reset_index()
fig6, ax6 = plt.subplots()
sns.lineplot(data=avg_hour_group, x="hr", y="registered", label="Registered", ax=ax6)
sns.lineplot(data=avg_hour_group, x="hr", y="casual", label="Casual", ax=ax6)
ax6.set_title("Average Hourly Users")
ax6.set_xlabel("Hour")
ax6.set_ylabel("Average Number of Users")
ax6.legend()
st.pyplot(fig6)
