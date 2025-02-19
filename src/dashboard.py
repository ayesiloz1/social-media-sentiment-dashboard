# src/dashboard.py

import streamlit as st
import pandas as pd
from visualization import (
    plot_sentiment_distribution,
    plot_sentiment_correlation,
    plot_sentiment_over_time,
    plot_keyword_frequency,
    plot_entity_frequency,
    plot_topic_distribution
)

def local_css(file_name):
    """Inject local CSS from a file."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.title("Social Media Sentiment Analysis Dashboard")
    st.markdown("## Explore Trends, Sentiment, Entities & Topics")
    
    # Inject custom CSS (optional if you have style.css)
    # local_css("src/style.css")
    
    # Load the master CSV (ensure it has the columns: id, text, created_at, author_id, etc.)
    data_path = "data/processed/tweets_master.csv"
    st.markdown(f"**Data Source:** `{data_path}`")
    df = pd.read_csv("data/processed/tweets_master.csv")
    print(df.columns)

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        st.error(f"File not found at {data_path}")
        return
    if df.empty:
        st.warning("The CSV is empty. Please verify your data collection and preprocessing.")
        return
    
    # Convert created_at to datetime and remove timezone information
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.tz_localize(None)
    
    # Create discrete sentiment label if missing
    if 'vader_compound' in df.columns and 'vader_label' not in df.columns:
        df['vader_label'] = df['vader_compound'].apply(
            lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral')
        )
    
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Date range filter
    if 'created_at' in df.columns:
        min_date = df['created_at'].min()
        max_date = df['created_at'].max()
        if pd.notnull(min_date) and pd.notnull(max_date):
            start_date, end_date = st.sidebar.date_input(
                "Select Date Range:",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
            if start_date > end_date:
                st.sidebar.error("Start date must be <= end date.")
            else:
                df = df[(df['created_at'] >= pd.to_datetime(start_date)) &
                        (df['created_at'] <= pd.to_datetime(end_date))]
    
    # Sentiment filter
    if 'vader_label' in df.columns:
        sentiment_options = ['positive', 'neutral', 'negative']
        selected_sentiments = st.sidebar.multiselect("Select Sentiment(s):", sentiment_options, default=sentiment_options)
        df = df[df['vader_label'].isin(selected_sentiments)]
    
    # Topic filter
    if 'dominant_topic' in df.columns:
        unique_topics = sorted(df['dominant_topic'].dropna().unique())
        selected_topic = st.sidebar.selectbox("Select a Topic (optional):", ["(All)"] + [str(t) for t in unique_topics])
        if selected_topic != "(All)":
            df = df[df['dominant_topic'] == int(selected_topic)]
    
    # Keyword filter
    if 'keywords' in df.columns:
        all_keywords = set()
        for row in df['keywords'].dropna():
            for kw in row.split(','):
                if kw.strip():
                    all_keywords.add(kw.strip())
        if all_keywords:
            chosen_keyword = st.sidebar.selectbox("Filter by Keyword:", ["(None)"] + sorted(all_keywords))
            if chosen_keyword != "(None)":
                df = df[df['keywords'].apply(lambda x: chosen_keyword in x if isinstance(x, str) else False)]
    
    # Show raw data option (excluding 'id' and 'author_id')
    if st.checkbox("Show raw data"):
        columns_to_hide = {'id', 'author_id','created_at','text','entities'}
        columns_to_show = [col for col in df.columns if col not in columns_to_hide]
        st.write(df[columns_to_show].head(50))
    
    # Layout: Use columns to display charts side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution (Numeric)")
        if 'vader_compound' in df.columns:
            fig1 = plot_sentiment_distribution(df, 'vader_compound')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No 'vader_compound' column found.")
        
        st.subheader("Keyword Frequency")
        if 'keywords' in df.columns:
            try:
                fig_kw = plot_keyword_frequency(df, 'keywords')
                st.plotly_chart(fig_kw, use_container_width=True)
            except ValueError as e:
                st.warning(str(e))
        else:
            st.info("No 'keywords' column available.")
    
    with col2:
        st.subheader("Sentiment Correlation (VADER vs. TextBlob)")
        if 'vader_compound' in df.columns and 'textblob_sentiment' in df.columns:
            fig_corr = plot_sentiment_correlation(df, 'vader_compound', 'textblob_sentiment')
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Missing sentiment columns for correlation.")
        
        st.subheader("Sentiment Over Time")
        if 'created_at' in df.columns and 'vader_compound' in df.columns:
            fig_time = plot_sentiment_over_time(df, date_col='created_at', sentiment_col='vader_compound', freq='H')
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("Need 'created_at' and 'vader_compound' for time series.")
    
    st.subheader("Entity Frequency")
    if 'entities' in df.columns:
        try:
            fig_ent = plot_entity_frequency(df, 'entities')
            st.plotly_chart(fig_ent, use_container_width=True)
        except ValueError as e:
            st.warning(str(e))
    else:
        st.info("No 'entities' column available.")
    

if __name__ == "__main__":
    main()
