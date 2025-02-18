import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk

# Ensure required NLTK data is downloaded
nltk.download('vader_lexicon')

# Initialize VADER once to improve performance
sia = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text):
    """
    Analyzes sentiment using NLTK's VADER.
    Returns a dictionary with scores.
    """
    return sia.polarity_scores(text)

def analyze_sentiment_textblob(text):
    """
    Analyzes sentiment using TextBlob.
    Returns the polarity score.
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity

def process_tweets_sentiment(df, text_column='cleaned_text'):
    """
    Applies sentiment analysis to a DataFrame column and returns a DataFrame with sentiment scores.
    """
    df['vader_scores'] = df[text_column].apply(analyze_sentiment_vader)
    # Optionally, extract the compound score directly
    df['vader_compound'] = df['vader_scores'].apply(lambda x: x['compound'])
    df['textblob_sentiment'] = df[text_column].apply(analyze_sentiment_textblob)
    return df

if __name__ == "__main__":
    # Example: Load your processed tweets CSV
    input_path = "data/processed/tweets_cleaned.csv"
    df = pd.read_csv(input_path)
    
    # Process sentiment analysis
    df = process_tweets_sentiment(df)
    
    # Optionally, save the results
    output_path = "data/processed/tweets_sentiment.csv"
    df.to_csv(output_path, index=False)
    
    # Print a sample of the output
    print(df.head())
