# src/nlp/topic_modeling.py
from gensim import corpora, models
import nltk
from nltk.corpus import stopwords

# Ensure the stopwords corpus is downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_for_lda(texts):
    """
    Tokenizes texts and removes stop words for topic modeling.
    
    Parameters:
        texts (list): A list of text strings.
        
    Returns:
        list: A list of token lists.
    """
    tokenized_texts = [
        [word for word in text.lower().split() if word not in stop_words]
        for text in texts
    ]
    return tokenized_texts

def perform_lda(tokenized_texts, num_topics=5):
    """
    Performs LDA topic modeling on the tokenized texts.
    
    Parameters:
        tokenized_texts (list): A list of token lists.
        num_topics (int): Number of topics to extract.
    
    Returns:
        tuple: (lda_model, dictionary, corpus)
    """
    dictionary = corpora.Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    return lda_model, dictionary, corpus

# Example usage for testing
if __name__ == "__main__":
    sample_texts = [
        "Apple is releasing a new iPhone next month",
        "Microsoft launches the latest version of Surface",
        "Google updates its search algorithm regularly"
    ]
    tokenized = preprocess_for_lda(sample_texts)
    lda_model, dictionary, corpus = perform_lda(tokenized, num_topics=3)
    topics = lda_model.print_topics(num_words=5)
    print("LDA Topics:")
    for topic in topics:
        print(topic)
