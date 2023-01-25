import logging

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, mean_absolute_error,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
NB_CORES = -1

mlflow.set_tracking_uri('http://mlflow:5000')

try:
    # Creating an experiment 
    mlflow.create_experiment('credit_scoring')
except:
    pass
# Setting the environment with the created experiment
mlflow.set_experiment('credit_scoring')


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

    

    df.drop('issue_d', axis=1, inplace=True)
    feature = df.columns[:-1]

    y = pd.factorize(df['charged_off'])[0]
    X = df[feature]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    with mlflow.start_run(run_name='RandomForest'):
        for key, value in rf_parameters.items():
            mlflow.log_param(key, value)
        
        model = RandomForestClassifier(
            **rf_parameters,
            random_state=RANDOM_SEED,
            n_jobs=NB_CORES,
        )

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

        mlflow.log_metric('accuracy', accuracy)
        mlflow.log_metric('precision', precision)
        mlflow.log_metric('recall', recall)