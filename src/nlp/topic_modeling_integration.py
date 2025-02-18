# src/nlp/topic_modeling_integration.py
import pandas as pd
import os
from gensim import corpora, models
from topic_modeling import preprocess_for_lda, perform_lda  # Import functions from topic_modeling.py

def assign_dominant_topic(lda_model, corpus):
    """
    For each document in the corpus, assigns the dominant topic.
    Returns a list of dominant topic indices.
    """
    dominant_topics = []
    for doc_bow in corpus:
        doc_topics = lda_model.get_document_topics(doc_bow)
        dominant_topic = max(doc_topics, key=lambda x: x[1])[0] if doc_topics else -1
        dominant_topics.append(dominant_topic)
    return dominant_topics

def run_topic_modeling(input_csv, output_csv, num_topics=5):
    # Load cleaned tweets
    df = pd.read_csv(input_csv)
    
    if 'cleaned_text' not in df.columns:
        raise KeyError("DataFrame must have a 'cleaned_text' column for topic modeling.")
    
    texts = df['cleaned_text'].tolist()
    tokenized_texts = preprocess_for_lda(texts)
    
    lda_model, dictionary, corpus = perform_lda(tokenized_texts, num_topics=num_topics)
    
    # Optionally, print out topics
    topics = lda_model.print_topics(num_words=5)
    print("LDA Topics:")
    for topic in topics:
        print(topic)
    
    # Assign dominant topic to each tweet
    df['dominant_topic'] = assign_dominant_topic(lda_model, corpus)
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Dominant topics assigned and saved to {output_csv}")

if __name__ == "__main__":
    input_path = "data/processed/tweets_cleaned.csv"
    output_path = "data/processed/tweets_with_topics.csv"
    run_topic_modeling(input_path, output_path, num_topics=5)
