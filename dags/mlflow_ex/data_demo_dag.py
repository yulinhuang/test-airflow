# Building the DAG using the functions from data_process and model module
import datetime as dt
from airflow import DAG
from airflow.operators.python import PythonOperator
from mlflow_ex.data_process import *
from mlflow_ex.model import run_model

fig_path = 'fig'

# Declare Default arguments for the DAG
default_args = {
    'owner': 'atanu',
    'depends_on_past': False,
    'start_date': dt.datetime.strptime('2023-01-23T00:00:00', '%Y-%m-%dT%H:%M:%S'),
    'catchup': False,
    'provide_context': True
}

# creating a new dag
dag = DAG('mlflow_example', default_args=default_args, max_active_runs=1)

# Integrating different operatortasks in airflow dag
# Integrating read_data operator in airflow dag
read_table = PythonOperator(task_id='read_table', python_callable=read_data,
                            op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating data_report operator in airflow dag
data_report = PythonOperator(task_id='data_report', python_callable=data_report,
                             op_kwargs={'fig_path': fig_path}, dag=dag)
# # Integrating plots operator in airflow dag
# plots = PythonOperator(task_id='var_dist_plots', python_callable=plot_var_distributions,
#                        op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating train_test operator in airflow dag
train_test = PythonOperator(task_id='train_test', python_callable=make_train_test,
                            op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating model_run operator in airflow dag
model_run = PythonOperator(task_id='model_run', python_callable=run_model,
                           op_kwargs={'fig_path': fig_path}, dag=dag)

# Set the task sequence
read_table.set_downstream(data_report)
data_report.set_downstream(train_test)
train_test.set_downstream(model_run)