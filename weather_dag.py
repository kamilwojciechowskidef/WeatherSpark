from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests
import json
import os

# Parametry do API
API_KEY = "TWÓJ_KLUCZ_API"
CITY = "Warsaw"

default_args = {
    'owner': 'kamil',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_weather_data(**kwargs):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Zapisz do pliku JSON w folderze, do którego Airflow ma dostęp
    file_path = '/opt/airflow/data/weather.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f)

    print(f"Pobrano dane pogodowe i zapisano do {file_path}")

with DAG('weather_etl', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    task_fetch_weather = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather_data
    )

    # Uruchomienie PySpark w kontenerze spark przez docker-compose (przykład)
    task_run_spark = BashOperator(
        task_id='run_pyspark_job',
        bash_command='docker-compose run --rm spark spark-submit /opt/spark/app/process_weather.py'
    )

    task_fetch_weather >> task_run_spark
