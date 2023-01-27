import logging
import datetime

# Importing MLFlow
import mlflow
# As all the algorithms are from sklearn
import mlflow.sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             precision_score, recall_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

mlflow.set_tracking_uri('http://mlflow:5000')

try:
    # Creating an experiment 
    mlflow.create_experiment('mlflow_example')
except:
    pass
# Setting the environment with the created experiment
mlflow.set_experiment('mlflow_example')


def run_model(**kwargs):
    '''
    Run your modelling tasks here
    '''
    ti = kwargs['ti']
    data_sets = ti.xcom_pull(task_ids='train_test')
    logging.info('Running Model...')
    #mlflow.set_tracking_uri('http://mlflow:5000')
    models = [('LR', LogisticRegression(solver='liblinear', multi_class='ovr')), ('LDA', LinearDiscriminantAnalysis()),
              ('KNN', KNeighborsClassifier()), ('CART', DecisionTreeClassifier()), ('NB', GaussianNB()),
              ('SVM', SVC(gamma='auto'))]
    # evaluate each model in turn
    results = []
    names = []
    seed = int(datetime.datetime.utcnow().timestamp())

    for name, model in models:
        with mlflow.start_run(run_name=name):
            mlflow.log_param('random seed', seed)
            kfold = StratifiedKFold(n_splits=10, random_state=seed, shuffle=True)
            cv_results = cross_val_score(model, data_sets[0], data_sets[2], cv=kfold, scoring='accuracy')
            results.append(cv_results)
            names.append(name)
            # logging different metrics in mlflow
            mlflow.log_metric('mean_cv_score_accuracy', cv_results.mean())
            mlflow.log_metric('std_cv_score_accuracy', cv_results.std())
            logging.info('%s model cross-validation performance: mean - %f , std - (%f)' % (name, cv_results.mean(),
                                                                                            cv_results.std()))
            model.fit(data_sets[0], data_sets[2])
            predictions = model.predict(data_sets[1])
            acc = accuracy_score(data_sets[3], predictions)
            cnfm = precision_score(data_sets[3], predictions,average= 'macro')
            cr = recall_score(data_sets[3], predictions, average= 'macro')
            # logging some more metrics in mlflow
            mlflow.log_metric('test_accuracy', acc)
            mlflow.log_metric('test_precision', cnfm)
            mlflow.log_metric('test_recall', cr)
            # logging the model as well
            mlflow.sklearn.log_model(model, name)
            logging.info('MLFlow has run, please check the mlflow UI')