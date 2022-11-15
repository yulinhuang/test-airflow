import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score, precision_score, recall_score

RANDOM_SEED = 42
NB_CORES = -1

def _model(data_task, transformer_task, **kwargs):
    df = kwargs['ti'].xcom_pull(task_ids=data_task)
    transformer = kwargs['ti'].xcom_pull(task_ids=transformer_task)

    rf_parameters = {
        "n_estimators": 125,
        "min_samples_split": 6,
        "min_samples_leaf": 2,
        "max_depth": 10,
        "bootstrap": True,
        "class_weight": "balanced",
    }

    model = RandomForestClassifier(
        **rf_parameters,
        random_state=RANDOM_SEED,
        n_jobs=NB_CORES,
    )

    df.drop('issue_d', axis=1, inplace=True)
    feature = df.columns[:-1]

    y = pd.factorize(df['charged_off'])[0]
    X = df[feature]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    model.fit(transformer.transform(X_train), y_train)

    # make predictions
    yhat = model.predict(transformer.transform(X_test))

    mae = mean_absolute_error(y_test, yhat)
    print('MAE: %.3f' % mae)
    accuracy = accuracy_score(y_test, yhat)
    print('accuracy: %.3f' % accuracy)
    precision = precision_score(y_test, yhat)
    print('precision: %.3f' % precision)
    recall = recall_score(y_test, yhat)
    print('recall: %.3f' % recall)
