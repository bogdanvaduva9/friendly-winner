def remove_stopwords(data, stopwords_filepath):
    with open(stopwords_filepath, 'r', encoding="utf-8") as file:
        content = file.read()
    stopwords = content.split("\n")
    processed_data = []
    for review in data:
        processed_article = ' '.join([w for w in review.split() if w not in stopwords])
        processed_data.append(processed_article)

    return processed_data


def remove_punctuation_signs(data):
    for idx, review in enumerate(data):
        for char in ",./<>?;\':\"[]\\{}|!@#$%^&*()-_+=~`":
            review = review.replace(char, " ")
        data[idx] = review

    return data


def remove_ro_chars(data):
    chars = [
        ('ș', 's'),
        ('ț', 't'),
        ('ă', 'a'),
        ('î', 'i'),
        ('â', 'a'),
        ('ţ', 't'),
        ('í', 'i'),
        ('à', 'a'),
        ('à', 'a'),
        ('ş', 's'),
        ('č', 'c'),
        ('ã', 'a'),
        ('ü', 'u'),
        ('è', 'e'),
    ]
    final_texts = []
    for text in data:
        for char in chars:
            text = text.replace(char[0], char[1])
        final_texts.append(text)

    return final_texts
