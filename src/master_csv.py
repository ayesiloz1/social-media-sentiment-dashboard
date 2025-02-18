import pandas as pd

df_sentiment = pd.read_csv("data/processed/tweets_sentiment.csv")
df_entities = pd.read_csv("data/processed/tweets_with_entities.csv")
df_topics = pd.read_csv("data/processed/tweets_with_topics.csv")

# Merge them on 'id' (assuming each file has an 'id' column)
df_merged = df_sentiment.merge(df_entities[['id','entities']], on='id', how='left')
df_merged = df_merged.merge(df_topics[['id','dominant_topic']], on='id', how='left')

df_merged.to_csv("data/processed/tweets_master.csv", index=False)
