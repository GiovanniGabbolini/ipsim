'''
Created on Thu Jan 30 2020

@author: https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
'''

# importing libraries
from nltk.tokenize import sent_tokenize
from src.text_processing.preprocess_word import stem, lower, stop
from src.text_processing.preprocess_phrase import tokenize


def _create_dictionary_table(text_string) -> dict:
    words = tokenize(text_string, [], [stem, lower, stop])

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:

    # algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]
                                    ] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]
                                    ] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]
                                                        ] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:

    # calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold,):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1
            if sentence_counter == 2:
                break

    return article_summary


def summarize(text):
    """very basic algorithm based on word frequencies. it extracts a number of phrases from a text

    Arguments:
        text {[string]} -- 

    """
    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(text)

    # tokenizing the sentences
    sentences = sent_tokenize(text)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(
        sentences, sentence_scores, 0.7 * threshold)

    return article_summary
