import datetime as dt
import os
import sys
import airflow.models
from airflow.operators.bash import BashOperator
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

path = 'opt/airflow_hw'
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)


from modules.pipeline import pipeline
from modules.predict import predict
# <YOUR_IMPORTS>

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2024, 12, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction_1',
        schedule_interval="00 15 * * *",
        default_args=args,
) as dag:
    first = BashOperator(
        task_id='welcome',
        bash_command='echo "welcome!"',
        dag=dag
    )
    pipeline = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
        dag=dag
    )
    predict = PythonOperator(
        task_id='predict',
        python_callable=predict,
        dag=dag
    )
    # <YOUR_CODE>
    first >> pipeline >> predict
