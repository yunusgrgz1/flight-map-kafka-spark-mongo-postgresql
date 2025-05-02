from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import logging
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../plugins')))


from insert_data_into_postgres import get_and_insert_data

logger = logging.getLogger('dag_logger')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025,4,14)
}

dag = DAG(
    dag_id="flights_dag",
    default_args=default_args,
    schedule_interval="@daily",
    "catchup": False,
    max_active_runs=1
)

def start_job():
    logging.info("Starting the pipeline.")

def fetch_data_from_mongo():
    try:
        logger.info("Fetching data from MongoDB")
        get_and_insert_data()

    except Exception as e:
        logger.error(f"An error occured while fetching data {e}")

def end_job():
    logger.info("Data has been inserted into Postgresql.")


start_task = PythonOperator(
    task_id='start_job',
    python_callable=start_job,
    dag=dag
)

fetching_data_task = PythonOperator(
    task_id='fetch_data_job',
    python_callable=fetch_data_from_mongo,
    dag=dag
)

end_task = PythonOperator(
    task_id= 'end_job',
    python_callable=end_job,
    dag=dag
)

start_task >> fetching_data_task >> end_task