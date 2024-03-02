import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#create_sum_inseason_day_df() digunakan untuk menyiapkan sum_inseason_day_df.
def create_sum_inseason_day_df(df):
    sum_inseason_day_df = df.groupby("season").cnt.sum().reset_index().sort_values(by="cnt", ascending=False)
    return sum_inseason_day_df

#create_sum_inseason_hour_df() digunakan untuk menyiapkan sum_inseason_hour_df.
def create_sum_inseason_hour_df(df):
    sum_inseason_hour_df = df.groupby("season").cnt.sum().reset_index().sort_values(by="cnt", ascending=False)
    return sum_inseason_hour_df

#create_weathersit_day_df() digunakan untuk menyiapkan weathersit_day_df.
def create_weathersit_day_df(df):
    weathersit_day_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    weathersit_day_df.rename(columns={
        "cnt": "cnt_sum"
    }, inplace=True)
    return weathersit_day_df

#create_weathersit_hour_df() digunakan untuk menyiapkan weathersit_hour_df.
def create_weathersit_hour_df(df):
    weathersit_hour_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    weathersit_hour_df.rename(columns={
        "cnt": "cnt_sum"
    }, inplace=True)
    return weathersit_hour_df

#create_yr_day_df() digunakan untuk menyiapkan yr_day_df.
def create_yr_day_df(df):
    yr_day_df = df.groupby(by="yr").agg({
        "cnt": "sum"
    }).reset_index()
    return yr_day_df

#create_yr_hour_df() digunakan untuk menyiapkan yr_hour_df.
def create_yr_hour_df(df):
    yr_hour_df = df.groupby(by="yr").agg({
        "cnt": "sum"
    }).reset_index()
    return yr_hour_df

#create_hr_df() digunakan untuk menyiapkan hr_df.
def create_hr_df(df):
    hr_df = df.groupby(by="hr").cnt.sum().reset_index()
    hr_df.rename(columns={
        "cnt": "cnt_sum"
    }, inplace=True)
    return hr_df

#load berkas .csv
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

datetime_columns = ["dteday"]
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

#membuat komponen filter day_df
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://images.app.goo.gl/MeVFN51t5ppJ5eZB6")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        key="date_input1"
    )

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

sum_inseason_day_df=create_sum_inseason_day_df(main_day_df)
weathersit_day_df=create_weathersit_day_df(main_day_df)
yr_day_df=create_yr_day_df(main_day_df)

#membuat komponen filter hour_df
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://images.app.goo.gl/MeVFN51t5ppJ5eZB6")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        key="date_input2"
    )
    
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

sum_inseason_hour_df=create_sum_inseason_hour_df(main_hour_df)
weathersit_hour_df=create_weathersit_hour_df(main_hour_df)
yr_hour_df=create_yr_hour_df(main_hour_df)
hr_df=create_hr_df(main_hour_df)

#melengkapi dashboard dengan berbagai visualisasi data
st.header('Bike Sharing Dashboard :sparkles:')

st.subheader("Musim dengan jumlah penyewaan sepeda tertinggi dan terendah (day)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors1 = ["#D3D3D3", "#D3D3D3", "#1D3557", "#D3D3D3"]
colors2 = ["#1D3557", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="season", y="cnt", data=sum_inseason_day_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('season', fontsize=30)
ax[0].set_title("Musim sewa tertinggi", loc="center", fontsize=50)
ax[0].tick_params(axis ='x', labelsize=35)
ax[0].tick_params(axis ='y', labelsize=30)

sns.barplot(x="season", y="cnt", data=sum_inseason_day_df.sort_values(by="cnt", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('season', fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Musim sewa terendah", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].tick_params(axis='y', labelsize=30)

st.pyplot(fig)
st.text('Keterangan arti sumbu x:\n'
        '- 1: springer\n'
        '- 2: summer\n'
        '- 3: fall\n'
        '- 4: winter')

st.subheader("Musim dengan jumlah penyewaan sepeda tertinggi dan terendah (hour)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors1 = ["#D3D3D3", "#D3D3D3", "#1D3557", "#D3D3D3"]
colors2 = ["#1D3557", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="season", y="cnt", data=sum_inseason_hour_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('season', fontsize=30)
ax[0].set_title("Musim sewa tertinggi", loc="center", fontsize=50)
ax[0].tick_params(axis ='x', labelsize=35)
ax[0].tick_params(axis ='y', labelsize=30)

sns.barplot(x="season", y="cnt", data=sum_inseason_hour_df.sort_values(by="cnt", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('season', fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Musim sewa terendah", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].tick_params(axis='y', labelsize=30)

st.pyplot(fig)
st.text('Keterangan arti sumbu x:\n'
        '- 1: springer\n'
        '- 2: summer\n'
        '- 3: fall\n'
        '- 4: winter')
with st.expander("See explanation"):
    st.write(
        """Berdasarkan data per hari (day) dan per jam (hour), jumlah sepeda paling banyak disewa, yaitu pada season 3 (fall) dan  jumlah sepeda yang paling sedikit disewa, yaitu pada season 1 (springer).
        """
    )

st.subheader("Jumlah sepeda sewaan berdasarkan weathersit")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors1 = ["#1D3557", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="cnt_sum", 
        x="weathersit",
        data=weathersit_day_df.sort_values(by="cnt_sum", ascending=False),
        palette=colors1,
        ax=ax
    )
    ax.set_title("per hari (day)", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors2 = ["#1D3557", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt_sum", 
        x="weathersit",
        data=weathersit_hour_df.sort_values(by="cnt_sum", ascending=False),
        palette=colors2,
        ax=ax
    )
    ax.set_title("per jam (hour)", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
st.text('Keterangan arti sumbu x:\n'
        '- 1: Clear, Few clouds, Partly cloudy, Partly cloudy\n'
        '- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist\n'
        '- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds\n'
        '- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog')
with st.expander("See explanation"):
    st.write(
        """Jumlah sepeda sewaan terbanyak berdasarkan weathersit, yaitu paling banyak pada weathersit 1 (Clear, Few clouds, Partly cloudy, Partly cloudy). Adapun visualisasi barplot semakin menurun menandakan bahwa semakin buruk weathersit maka sepeda yang dipinjam semakin sedikit. Hal tersebut menunjukkan bahwa weathersit lumayan berpengaruh terhadap jumlah sepeda sewaan baik itu per hari (day) maupun per jam (hour).
        """
    )
 
st.subheader('Peminjaman sepeda 2011-2012 (day)')
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    yr_day_df["yr"],
    yr_day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.text('Keterangan arti sumbu x:\n'
        '- 0: tahun 2011\n'
        '- 1: tahun 2012')


st.subheader('Peminjaman sepeda 2011-2012 (hour)')
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    yr_day_df["yr"],
    yr_day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.text('Keterangan arti sumbu x:\n'
        '- 0: tahun 2011\n'
        '- 1: tahun 2012')
with st.expander("See explanation"):
    st.write(
        """Hasil visualisasi data per hari (day) dan per jam (hour) menunjukkan bahwa dari tahun 2011 hingga 2012 terjadi peningkatan dalam peminjaman sepeda. Terlihat bahwa jumlah peminjaman sepeda pada tahun 2012 lebih banyak daripada jumlah peminjaman sepeda pada tahun 2011.
        """
    )

st.subheader("Peminjaman sepeda terbanyak berdasarkan jam (hr)")

fig, ax = plt.subplots(figsize=(20, 10))

colors = ["#1D3557" if hr == hr_df["hr"].index[17] else "#D3D3D3" for hr in hr_df["hr"]]

sns.barplot(
    y="cnt_sum", 
    x="hr",
    data=hr_df.sort_values(by="cnt_sum", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("per jam (hour)", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
with st.expander("See explanation"):
    st.write(
        """Hasil visualisasi data per jam (hour) menunjukkan bahwa jumlah peminjaman sepeda terbanyak berdasarkan jam, yaitu pada saat hr=17.
        """
    )
