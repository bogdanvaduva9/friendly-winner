from typing import List

from data_tools.rating_object import RatingObject


def data_distribution(data: List[RatingObject]):
    distribution = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    for rating in data:
        distribution[rating.rating] += 1

    percentage_distribution = {
        k: v / len(data) * 100 for k, v in distribution.items()
    }

    print(f"ITEMS NUMBERS\n"
          f"1: {distribution[1]}\n"
          f"2: {distribution[2]}\n"
          f"3: {distribution[3]}\n"
          f"4: {distribution[4]}\n"
          f"5: {distribution[5]}\n")
    print(f"ITEMS PERCENTAGES\n"
          f"1: {round(percentage_distribution[1], 2)}\n"
          f"2: {round(percentage_distribution[2], 2)}\n"
          f"3: {round(percentage_distribution[3], 2)}\n"
          f"4: {round(percentage_distribution[4], 2)}\n"
          f"5: {round(percentage_distribution[5], 2)}\n")


def confusion_matrix_sort_of(predictions, y_test):
    correct = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    incorrect = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    total = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    for i in range(len(predictions)):
        if predictions[i] == y_test[i]:
            correct[predictions[i]] += 1
        else:
            incorrect[predictions[i]] += 1
        total[predictions[i]] += 1
    incorrect_statistics = {
        k: round(v / total[k] * 100, 2) for k, v in incorrect.items()
    }
    correct_statistics = {
        k: round(v / total[k] * 100, 2) for k, v in correct.items()
    }
    print("INCORRECT: ", incorrect_statistics)
    print("CORRECT: ", correct_statistics)
