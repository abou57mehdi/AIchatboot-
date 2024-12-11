# preprocessing.py
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer  # Changed to French stemmer

nltk.download('punkt')
nltk.download("stopwords")

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation but keep spaces
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words("french"))
    tokens = [word for word in tokens if word not in stop_words]
    
    # French stemming instead of lemmatization
    stemmer = FrenchStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return ' '.join(tokens)

