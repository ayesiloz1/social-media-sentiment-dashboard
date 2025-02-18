# Social Media Sentiment Analysis Dashboard

This project is an end-to-end pipeline for analyzing social media sentiment using Twitter data. It demonstrates data collection, cleaning, multiple NLP techniques, and interactive visualizations—all wrapped up in an easy-to-use Streamlit dashboard.

## Features

- **Data Preprocessing:**  
  Cleans raw tweets by removing URLs, retweet indicators, mentions, emojis, and extra whitespace. Also extracts keywords (hashtags) from tweets.

- **Sentiment Analysis:**  
  Uses NLTK VADER and TextBlob to analyze tweet sentiment. Creates numeric sentiment scores and discrete labels (positive, neutral, negative).

- **Named Entity Recognition (NER):**  
  Uses spaCy to extract named entities from tweet text, allowing analysis of frequently mentioned organizations, people, or locations.

- **Topic Modeling:**  
  Implements Latent Dirichlet Allocation (LDA) via gensim to automatically cluster tweets into topics.

- **Interactive Dashboard:**  
  A Streamlit dashboard with multiple interactive Plotly visualizations, including:
  - Sentiment distribution (numeric & label)
  - Sentiment correlation (VADER vs. TextBlob)
  - Sentiment over time
  - Keyword frequency
  - Entity frequency
  - Topic distribution

## Project Structure

social-media-sentiment-dashboard/
├── data/
│   ├── raw/                    # Raw tweet data (not shared publicly)
│   └── processed/              # Processed CSV files (tweets_master.csv, etc.)
├── src/
│   ├── dashboard.py            # Streamlit dashboard for interactive visualizations
│   ├── visualization.py        # Plotly visualization functions
│   ├── preprocessing.py        # Data cleaning and keyword extraction script
│   └── nlp/
│       ├── sentiment_analysis.py   # Sentiment analysis functions (VADER and TextBlob)
│       ├── ner.py                  # Named Entity Recognition using spaCy
│       ├── topic_modeling.py       # Topic modeling functions using gensim LDA
│       └── topic_modeling_integration.py  # Integration script for topic modeling on tweets
│   └── style.css               # Custom CSS for dashboard styling
├── .gitignore                  # Files and folders to ignore in Git (e.g., raw data, virtual env)
└── README.md                   # This documentation file


## How to Run

### 1. Set Up the Environment

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/yourusername/social-media-sentiment-dashboard.git
cd social-media-sentiment-dashboard
python -m venv venv
```