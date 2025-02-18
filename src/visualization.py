# src/visualization.py

import plotly.express as px
import pandas as pd
import ast

def plot_sentiment_distribution(df, sentiment_col='vader_compound'):
    """
    Creates a histogram of numeric sentiment scores.
    """
    if sentiment_col not in df.columns:
        raise ValueError(f"Column '{sentiment_col}' not found in DataFrame.")
    
    fig = px.histogram(
        df,
        x=sentiment_col,
        nbins=20,
        title=f"Distribution of {sentiment_col}",
        template="plotly_dark",  # using a dark template for a modern look
        color_discrete_sequence=["#2ca02c", "#7f7f7f", "#d62728"]
    )
    fig.update_layout(
        xaxis_title=f"{sentiment_col} Score",
        yaxis_title="Count",
        font=dict(color="white"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def plot_sentiment_labels(df, label_col='vader_label'):
    """
    Creates a bar chart of sentiment labels (positive, neutral, negative).
    """
    if label_col not in df.columns:
        raise ValueError(f"Column '{label_col}' not found in DataFrame.")
    
    fig = px.histogram(
        df,
        x=label_col,
        color=label_col,
        title="Sentiment Label Distribution",
        template="plotly_dark",
        color_discrete_sequence=["#d62728", "#7f7f7f", "#2ca02c"]
    )
    return fig

def plot_sentiment_correlation(df, col1='vader_compound', col2='textblob_sentiment'):
    """
    Creates a scatter plot comparing two sentiment scores with a trendline.
    """
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Columns '{col1}' or '{col2}' not found in DataFrame.")
    
    fig = px.scatter(
        df,
        x=col1,
        y=col2,
        title=f"{col1} vs. {col2}",
        labels={col1: col1, col2: col2},
        trendline="ols",
        template="plotly_dark"
    )
    return fig

def plot_sentiment_over_time(df, date_col='created_at', sentiment_col='vader_compound', freq='H'):
    """
    Creates a line chart showing average sentiment over time.
    Groups by the specified frequency.
    """
    if date_col not in df.columns:
        raise ValueError(f"Column '{date_col}' not found in DataFrame.")
    if sentiment_col not in df.columns:
        raise ValueError(f"Column '{sentiment_col}' not found in DataFrame.")
    
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.tz_localize(None)
    sentiment_time = (
        df.dropna(subset=[date_col, sentiment_col])
          .groupby(pd.Grouper(key=date_col, freq=freq))[sentiment_col]
          .mean()
          .reset_index()
    )
    
    fig = px.line(
        sentiment_time,
        x=date_col,
        y=sentiment_col,
        title=f"Average {sentiment_col} Over Time",
        labels={date_col: 'Time', sentiment_col: 'Average Sentiment'},
        template="plotly_dark"
    )
    return fig

def plot_keyword_frequency(df, keyword_col='keywords'):
    """
    Creates a bar chart showing the frequency of keywords (assumed comma-separated).
    """
    if keyword_col not in df.columns:
        raise ValueError(f"Column '{keyword_col}' not found in DataFrame.")
    
    def parse_keywords(x):
        if isinstance(x, str):
            return [kw.strip() for kw in x.split(',') if kw.strip()]
        return []
    
    df[keyword_col] = df[keyword_col].apply(parse_keywords)
    all_keywords = [kw for sublist in df[keyword_col] for kw in sublist]
    if not all_keywords:
        raise ValueError("No keywords found in the DataFrame.")
    
    keyword_counts = pd.Series(all_keywords).value_counts().reset_index()
    keyword_counts.columns = ['keyword', 'count']
    
    fig = px.bar(
        keyword_counts.head(15),
        x='keyword',
        y='count',
        title="Top Keywords",
        labels={'keyword': 'Keyword', 'count': 'Count'},
        template="plotly_dark"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_entity_frequency(df, entity_col='entities'):
    """
    Creates a bar chart showing the most frequent named entities.
    Expects entities to be stored as a string representation of a list.
    """
    if entity_col not in df.columns:
        raise ValueError(f"Column '{entity_col}' not found in DataFrame.")
    
    def parse_entities(ents):
        if isinstance(ents, str):
            try:
                parsed = ast.literal_eval(ents)
                if isinstance(parsed, list):
                    return parsed
            except (ValueError, SyntaxError):
                return []
        elif isinstance(ents, list):
            return ents
        return []
    
    df[entity_col] = df[entity_col].apply(parse_entities)
    all_entities = []
    for row in df[entity_col]:
        for ent_tuple in row:
            if isinstance(ent_tuple, tuple) and len(ent_tuple) == 2:
                all_entities.append(ent_tuple[0])
    
    if not all_entities:
        raise ValueError("No valid entities found in the DataFrame.")
    
    entity_counts = pd.Series(all_entities).value_counts().reset_index()
    entity_counts.columns = ['entity', 'count']
    
    fig = px.bar(
        entity_counts.head(15),
        x='entity',
        y='count',
        title="Top Entities",
        labels={'entity': 'Entity', 'count': 'Count'},
        template="plotly_dark"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_topic_distribution(df, topic_col='dominant_topic'):
    """
    Creates a bar chart showing how many tweets fall into each topic.
    """
    if topic_col not in df.columns:
        raise ValueError(f"Column '{topic_col}' not found in DataFrame.")
    
    topic_counts = df[topic_col].value_counts().reset_index()
    topic_counts.columns = ['topic', 'count']
    
    fig = px.bar(
        topic_counts,
        x='topic',
        y='count',
        title="Topic Distribution",
        labels={'topic': 'Topic', 'count': 'Count'},
        template="plotly_dark"
    )
    return fig

if __name__ == "__main__":
    # Example DataFrame for testing
    df_test = pd.DataFrame({
        'vader_compound': [0.8, -0.3, 0.1, 0.5],
        'textblob_sentiment': [0.7, -0.1, 0.0, 0.3],
        'created_at': pd.date_range("2025-02-17 10:00", periods=4, freq='H'),
        'keywords': ["apple, banana", "banana", "", "apple, cherry, banana"],
        'entities': [
            "[('PhiladelphiaEagles', 'ORG')]",
            "[('kansascitychiefs', 'PERSON')]",
            "[]",
            "[('Philadelphia', 'GPE')]"
        ],
        'dominant_topic': [0, 1, 1, 0]
    })
    
    fig1 = plot_sentiment_distribution(df_test, 'vader_compound')
    fig1.show()

    fig2 = plot_sentiment_correlation(df_test)
    fig2.show()

    fig3 = plot_sentiment_over_time(df_test)
    fig3.show()

    fig4 = plot_keyword_frequency(df_test)
    fig4.show()

    fig5 = plot_entity_frequency(df_test)
    fig5.show()

    fig6 = plot_topic_distribution(df_test)
    fig6.show()
