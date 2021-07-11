import pandas as pd
from src.data import data
from src.text_processing.preprocess_word import lower, lemma
from src.utils.timing import tick, tock

_d = None


def word_concreteness(word):
    """Return a word concreteness score from 0 to 5, or -1 if we cannot assign a score
       Eg: Wood is concrete, love is not

       Source: http://crr.ugent.be/archives/1330

    Args:
        word (str): word

    Returns:
        int: concr score
    """
    global _d
    if _d is None:
        _df = pd.read_csv(f"{data.preprocessed_dataset_path}/concreteness.csv")
        keys = _df["Word"].values
        values = _df["Conc.M"].values
        _d = dict(zip(keys, values))

    word_preprocessed = lemma(lower(word))

    try:
        concretenss = _d[word_preprocessed]
    except KeyError:
        concretenss = -1

    return concretenss


if __name__ == "__main__":
    word_concreteness("ball")
