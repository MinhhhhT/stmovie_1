import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Tao tieu de trang
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")

# read file
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
movies_data.info()
movies_data.duplicated()
movies_data.count()
movies_data.dropna()

# Tao sidebar loc du lieu tu dataset movies
genre_list = movies_data['genre'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
year_list = movies_data['year'].unique().tolist()

# Them sidebar 
with st.sidebar:
    st.write("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
    # Tao range slider de chon so diem
    filter_score_rating = st.slider(label="Choose a value:",
                                    min_value=1.0,
                                    max_value=10.0,
                                    value=(3.0, 4.0))
    
    st.write("Select your preferred genre(s) and year to view the movies released that year and on that genre")
    # Tao multiselect de chon the loai
    filter_genre_list = st.multiselect("Choose genre:", genre_list, default=['Drama', 'Adventure', 'Action', 'Comedy'])

    # Tao selectbox de chon nam
    filter_year = st.selectbox("Choose a year", year_list, 0)

# Tao bien luu tru du lieu sau khi loc
filtered_score_rating = (movies_data['score'].between(*filter_score_rating))

filtered_genre_year = (movies_data['genre'].isin(filter_genre_list)) & (movies_data['year'] == filter_year)

# Tao bang du lieu va bieu do duong
col1, col2 = st.columns([4, 6])
with col1: 
    st.write("#### Lists of movies filtered by year and genre")
    df_genre_year = movies_data[filtered_genre_year].groupby(['name', 'genre'])['year'].sum()
    df_genre_year = df_genre_year.reset_index()
    st.dataframe(df_genre_year, width = 390)

with col2: 
    st.write("#### User score of movies and their genre")
    rating_count_year = movies_data[filtered_score_rating].groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    fig = px.line(rating_count_year, x='genre', y='score')
    st.plotly_chart(fig)

# Tao bieu do cot bang matplotlib
st.markdown("Average Movie Budget, Grouped by Genre")
avg_budget_genre = movies_data.groupby('genre')['budget'].mean().round()
avg_budget_genre = avg_budget_genre.reset_index()
genre = avg_budget_genre['genre']
avg_budget = avg_budget_genre['budget']

fig = plt.figure(figsize=(19, 9))
plt.bar(genre, avg_budget, color='maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
st.pyplot(fig)


