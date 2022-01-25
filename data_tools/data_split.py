from nltk.stem import SnowballStemmer
from sklearn.model_selection import train_test_split

from data_tools.data_processing import remove_stopwords, remove_punctuation_signs, remove_ro_chars
from data_tools.statistics import data_distribution


def stem_texts(texts):
    stemmer = SnowballStemmer(language='romanian')
    final_texts = []
    for text in texts:
        final_text = " ".join([stemmer.stem(item) for item in text.split()])
        final_texts.append(final_text)

    return final_texts


def remove_reviews(data, rating: int, percentage_left: float):
    final_data = []
    five_star_review = []
    while data:
        review = data.pop()
        if review.rating == rating:
            five_star_review.append(review)
        else:
            final_data.append(review)

    final_data += five_star_review[0:int(percentage_left * len(five_star_review))]

    return final_data


def split_data(data, stopwords_filepath, test=False):
    labels = []
    texts = []
    ids = []
    if test:
        for review in data:
            labels.append(review.rating)
            ids.append(review.rating_id)
            text = " ".join([item.lower() for item in review.text.split() if len(item) > 1])
            text = " ".join([item for item in text.split() if item.isalpha()])
            texts.append(text)

        print("Removing stopwords")
        texts = remove_stopwords(texts, stopwords_filepath=stopwords_filepath)
        print("Removing punctuation signs")
        texts = remove_punctuation_signs(texts)
        texts = [" ".join(text.split()) for text in texts]
        print("Stemming")
        texts = remove_ro_chars(texts)
        texts = stem_texts(texts)

        return texts, labels, ids
    labels = []
    texts = []
    print("Removing 90 percent 5 star reviews")
    # data = remove_reviews(data, rating=5, percentage_left=0.2)
    # data = remove_reviews(data, rating=4, percentage_left=0.25)
    # data = remove_reviews(data, rating=3, percentage_left=0.5)
    # data = remove_reviews(data, rating=1, percentage_left=0.5)
    data_distribution(data)
    for review in data:
        labels.append(review.rating)
        text = " ".join([item.lower() for item in review.text.split() if len(item) > 1])
        text = " ".join([item for item in text.split() if item.isalpha()])
        texts.append(text)

    print("Removing stopwords")
    texts = remove_stopwords(texts, stopwords_filepath=stopwords_filepath)
    print("Removing punctuation signs")
    texts = remove_punctuation_signs(texts)
    texts = [" ".join(text.split()) for text in texts]
    print("Stemming")
    texts = remove_ro_chars(texts)
    texts = stem_texts(texts)

    x_train, x_test, y_train, y_test = train_test_split(texts, labels, random_state=42, shuffle=True)

    return x_train, x_test, y_train, y_test
