from dotenv import load_dotenv
import os
import tweepy
import pandas as pd
import time

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials and settings from the environment
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
QUERY = os.getenv("TWITTER_QUERY", "#PhiladelphiaEagles")
MAX_RESULTS = int(os.getenv("TWITTER_MAX_RESULTS", 10))

# Create a Tweepy Client instance for Twitter API v2 endpoints
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_recent_tweets(query, max_results=10, retry_count=0):
    """
    Fetches recent tweets matching the query using the Twitter API v2.
    Implements simple retry logic if a rate limit error occurs.
    Returns a list of dictionaries with tweet details.
    """
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "author_id"]
        )
        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_id": tweet.author_id
                })
        else:
            print("No tweets found for the query.")
        return tweets
    except tweepy.errors.TooManyRequests as e:
        # Rate limit error occurred
        retry_count += 1
        wait_time = 60  # default wait time in seconds (adjust if needed)
        print(f"Rate limit reached. Waiting for {wait_time} seconds before retrying... (Retry #{retry_count})")
        time.sleep(wait_time)
        return fetch_recent_tweets(query, max_results, retry_count)
    except Exception as e:
        print("Error fetching tweets:", e)
        return []

def save_tweets_to_csv(tweets, filepath):
    """
    Saves a list of tweet dictionaries to a CSV file.
    """
    if tweets:
        df = pd.DataFrame(tweets)
        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(tweets)} tweets to {filepath}")
    else:
        print("No tweets to save.")

if __name__ == "__main__":
    tweets = fetch_recent_tweets(QUERY, max_results=MAX_RESULTS)
    
    # Print tweets to the console
    for tweet in tweets:
        print(f"{tweet['id']} ({tweet['created_at']}): {tweet['text']}\n")
    
    output_path = os.path.join("data", "raw", "tweets.csv")
    save_tweets_to_csv(tweets, output_path)
