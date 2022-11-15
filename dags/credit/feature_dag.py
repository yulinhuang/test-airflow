from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from credit.src.model import _model
from credit.src.processing import _feature_engineering, _read_csv
from credit.src.transform import _transform

RAW_DATA_FOLDER = "data/raw/"
RAW_DATA_NAME = "raw_data.csv"
RAW_DATA_PATH = RAW_DATA_FOLDER + RAW_DATA_NAME

PROCESSED_DATA_FOLDER = "data/processed/"
PROCESSED_DATA_NAME = "lcld_v2.csv"
DATASET_PATH = PROCESSED_DATA_FOLDER + PROCESSED_DATA_NAME



with DAG(
    'feature-engineering',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
        # 'provide_context': True
    },
    description='Feature engineering DAG for credit scoring',
    schedule=timedelta(days=1),
    start_date=datetime(2022, 11, 11),
    catchup=False, 
    max_active_runs=1,
    tags=['feature', 'credit'],
) as dag:

    read_csv = PythonOperator(
        task_id = 'read_csv',
        python_callable=_read_csv,
        op_kwargs={'file_path': RAW_DATA_PATH},
        dag = dag
    )

    feature_engineering = PythonOperator(
        task_id = 'feature_engineering',
        python_callable=_feature_engineering,
        op_kwargs={
            'previous_task': 'read_csv',
            'save_path': DATASET_PATH},
        dag = dag
    )

    transformer = PythonOperator(
        task_id = 'transformer_task',
        python_callable=_transform,
        op_kwargs={
            'previous_task': 'feature_engineering'},
        dag = dag
    )

    model = PythonOperator(
        task_id = 'training',
        python_callable=_model,
        op_kwargs={
            'data_task': 'feature_engineering',
            'transformer_task': 'transformer_task'
        },
        dag = dag
    )

    read_csv >> feature_engineering >> transformer >> model


