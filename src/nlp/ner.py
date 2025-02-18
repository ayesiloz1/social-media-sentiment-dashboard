# src/nlp/ner.py

import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extracts named entities from the provided text.
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def run_ner_on_tweets(input_csv, output_csv):
    import pandas as pd
    import os
    # Load your cleaned tweets
    df = pd.read_csv(input_csv)
    
    # Ensure you have a column named 'cleaned_text'
    if 'cleaned_text' not in df.columns:
        raise KeyError("DataFrame must have a 'cleaned_text' column for NER.")
    
    # Use extract_entities defined above
    df['entities'] = df['cleaned_text'].apply(lambda text: extract_entities(text))
    
    # Save the updated DataFrame
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Entities extracted and saved to {output_csv}")

if __name__ == "__main__":
    input_path = "data/processed/tweets_cleaned.csv"
    output_path = "data/processed/tweets_with_entities.csv"
    run_ner_on_tweets(input_path, output_path)
