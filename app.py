import json
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score

from data_tools.data_split import split_data
from data_tools.rating_object import create_ratings
from data_tools.statistics import confusion_matrix_sort_of


# config = Config()
# mongo_repo = MongoRepository(db="phd", collection="friendly-winner")
# mongo_repo.connect()


# def grid_search(x, model_name, model, sparse_matrix=False):
#     print("Running for {}".format(model_name))
#     if sparse_matrix:
#         x = x.todense()
#     configs = config.get_configs(model_name)
#     if not configs:
#         raise AttributeError(f"Not available for {model_name}")
#     clf = GridSearchCV(model, configs, scoring='f1_weighted', n_jobs=7)
#     clf.fit(x, y_train)
#     new_best_score = {
#         "model_name": model_name,
#         "data": {
#             "parameters": clf.best_params_,
#             "score": clf.best_score_,
#             "date": str(datetime.now())
#         }
#     }
#     current_results = mongo_repo.get_one_by_key(model_name)
#     if current_results:
#         if current_results['data']["score"] < new_best_score['data']["score"]:
#             mongo_repo.update_one(new_best_score)
#     else:
#         mongo_repo.add_one(new_best_score)


def run_model(classifier, clf_name, x, test=False):
    start = time.time()
    classifier.fit(x_train_vectorized, y_train)
    pred = classifier.predict(x)
    if test:
        return pred
    print("{}: {:.2f}%".format(clf_name, f1_score(pred, y_val, average='weighted') * 100))
    confusion_matrix_sort_of(pred, y_val)
    print(f"took me {round(time.time() - start, 2)} to run {clf_name}\n")
    return pred


def get_ensemble_results(pred_len, results, y):
    overall_predictions = []
    for i in range(pred_len):
        predict_dict = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
        for result in results:
            predict_dict[result[i]] += 1
        initial_predict = 0
        final_key = 0
        for k, v in predict_dict.items():
            if v > initial_predict:
                final_key = k
        overall_predictions.append(final_key)
    print("{:.2f}".format(f1_score(overall_predictions, y, average='weighted') * 100))
    confusion_matrix_sort_of(overall_predictions, y)
    print(f"took me {time.time() - start} to run")


if __name__ == '__main__':
    train_ratings = create_ratings("data/train.json")
    test_ratings = create_ratings("data/test_wor.json")

    x_train, x_val, y_train, y_val = split_data(train_ratings, stopwords_filepath="data/stopwords.txt")
    x_test, y_test, ids = split_data(test_ratings, stopwords_filepath='data/stopwords.txt', test=True)

    vect = CountVectorizer(ngram_range=(1, 2), max_df=0.95).fit(x_train)
    x_train_vectorized = vect.transform(x_train)
    x_val_vectorized = vect.transform(x_val)
    x_test_vectorized = vect.transform(x_test)
    overall_results = []
    start = time.time()
    rf = RandomForestClassifier(n_jobs=5)
    # onevsrest = OneVsRestClassifier(LinearSVC(max_iter=10000))
    # mnb = MultinomialNB()
    # svc = SVC(kernel='rbf', decision_function_shape='ovo')
    # mlp = MLPClassifier(alpha=1, max_iter=1000, verbose=True, n_iter_no_change=3, early_stopping=True, tol=0.001)
    overall_results.append(run_model(rf, "RandomForest", x_val_vectorized))
    # overall_results.append(run_model(onevsrest, "OneVsRest", x_val_vectorized))
    # overall_results.append(run_model(mnb, "MultinomialNB", x_val_vectorized))
    # overall_results.append(run_model(svc, "SVC", x_val_vectorized))
    # overall_results.append(run_model(mlp, "MLP", x_val_vectorized))

    # get_ensemble_results(len(y_val), overall_results, y_val)
    preds = run_model(rf, "RandomForest", x_test_vectorized, test=True)
    objs = []
    for i in range(len(preds)):
        objs.append({
            "id": str(ids[i]),
            "review": str(x_test[i]),
            "pred": str(preds[i])
        })

    with open('test.json', 'w', encoding='utf-8') as file:
        file.write(
            json.dumps(
                {
                    "results": objs
                },
                indent=4
            )
        )
