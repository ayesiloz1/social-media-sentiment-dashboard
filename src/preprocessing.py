import pandas as pd
import re
import os

def extract_hashtags(text):
    """
    Extracts all hashtags from the raw text (e.g., #example)
    and returns them as a comma-separated string.
    """
    # Find hashtags using a regex capturing # followed by word characters
    hashtags = re.findall(r"#(\w+)", text)
    # Join the list of hashtags with commas, e.g. "example,hello"
    return ",".join(hashtags) if hashtags else ""

def clean_text(text):
    """
    Cleans the tweet text by removing URLs, RT indicators, mentions, 
    and non-ASCII characters, then converting to lowercase.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove RT (retweet indicator) at the beginning
    text = re.sub(r'^RT\s+', '', text)
    # Remove mentions (@username)
    text = re.sub(r'\@\w+', '', text)
    # Remove emojis and non-ASCII characters (optional)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_tweets(input_csv, output_csv):
    # Read the raw CSV file, explicitly specifying the delimiter and encoding
    df = pd.read_csv(input_csv, delimiter=',', encoding='utf-8-sig')
    
    # Remove any extra whitespace from column names
    df.columns = df.columns.str.strip()
    print("Columns in CSV:", df.columns)
    
    # Check if the expected column 'text' exists
    text_column = 'text'
    if text_column not in df.columns:
        raise KeyError(f"Expected column '{text_column}' not found. Available columns: {df.columns}")
    
    # 1. Extract hashtags from the original text and store them in a 'keywords' column
    df['keywords'] = df[text_column].apply(extract_hashtags)

    # 2. Clean the text
    df['cleaned_text'] = df[text_column].apply(clean_text)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    # Save the cleaned tweets to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Processed tweets saved to {output_csv}")

if __name__ == "__main__":
    input_path = os.path.join("data", "raw", "tweets.csv")
    output_path = os.path.join("data", "processed", "tweets_cleaned.csv")
    preprocess_tweets(input_path, output_path)
