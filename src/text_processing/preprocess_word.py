'''
Created on Sat Feb 01 2020

@author Giovanni Gabbolini
'''


from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


def stem(word):
    """apply PorterStemmer to word
       It returns the word always in lower case letters

    Arguments:
        word {string} -- 

    Returns:
        str -- preprocessed word
    """
    stem = PorterStemmer()
    return stem.stem(word)


def lower(word):
    """apply lower case to word

    Arguments:
        word {string} -- 

    Returns:
        str -- preprocessed word
    """
    return word.lower()


def stop(word):
    """converts a word to '' in case it is a stopword

    Arguments:
        word {string} -- 

    Returns:
        str -- preprocessed word
    """
    stop_words = set(stopwords.words("english"))
    return word if word not in stop_words else ''


def lemma(word):
    # This assumes that word is a noun. Otherwise, provide another argument to lemmatize function
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)
