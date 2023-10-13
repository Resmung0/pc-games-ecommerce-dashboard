from datetime import datetime

import streamlit as st
import altair as alt
import plotly.express as px

from src.etl.dashboard.transform import (
    visualize_os_column,
    visualize_game_mode_column,
    visualize_genre_column, 
    visualize_rate_column,
    visualize_drm_column, 
    visualize_price_column,
    visualize_publisher_column,
    visualize_developer_column
)
from src.etl.dashboard.extract import extract_nuuvem_data


st.set_page_config(page_title='PC Games E-commerce', page_icon='🎮', layout='wide')

with st.sidebar:
    st.title('PC Games E-commerce Dashboard')
    st.divider()
    
    platforms = ['☁️ Nuuvem', '🐧 Kinguin', '👽 Green Man Gaming', '🎮 Hype']
    platforms = st.multiselect(
        'Choose the platforms to analyse',
        platforms, 
        default='☁️ Nuuvem', 
        placeholder='Click and choose an option',
        
    )


# Get datasets
df = extract_nuuvem_data()

# Web-app layout
tab_1, tab_2 = st.tabs(['Game specifics', 'System specifics'])

with tab_1:
    game_mode_column, genre_column = st.columns(2)
    with st.container():
        with game_mode_column:
            st.write('Top 5 game modes')
            st.bar_chart(visualize_game_mode_column(df))

        with genre_column:
            st.write('Top 5 game genre')
            st.bar_chart(visualize_genre_column(df))
        
        st.write('Ratings distribution')
        st.bar_chart(visualize_rate_column(df))
        
        st.write('Games ages distribution')
        chart = df.assign(game_age=(datetime.now().year - df.release_date.dt.year))
        chart = (
            alt.Chart(chart)
                .transform_window(proportions="cume_dist()", sort=[{"field": "game_age"}])
                .mark_line(interpolate="step-after")
                .encode(x="game_age:Q", y="proportions:Q")
        )
        st.altair_chart(chart, True)
        
    
with tab_2:
    os_column, drm_column = st.columns(2)
    publisher_column, developer_column = st.columns(2)
    
    with st.container():        
        with os_column:
            st.write('Most Popular Operating Systems')
            data = visualize_os_column(df)    
            configs = {'radialaxis': {'visible': True}, 'bgcolor': '#1e2031'}
            fig = px.line_polar(data, r=data.values, theta=data.index, line_close=True)
            fig.update_traces(fill='toself').update_layout(polar=configs, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        with drm_column:
            st.write('Most Popular Game Platforms')
            st.bar_chart(visualize_drm_column(df))
        
        with publisher_column:
            st.write('Top 10 Game Publishers')
            st.bar_chart(visualize_publisher_column(df))
    
        with developer_column:
            st.write('Top 10 Game Developers')
            st.bar_chart(visualize_developer_column(df))
        
        st.write('Games price distribution')
        kde = visualize_price_column(df)
        st.altair_chart(kde, True)
        

