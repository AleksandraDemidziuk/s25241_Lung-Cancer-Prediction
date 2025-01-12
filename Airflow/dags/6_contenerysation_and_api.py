from datetime import timedelta, datetime

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# Funkcja tworząca API pobierająca model
def creat_API(**kwargs):
    print()


# Funkcja opakowująca API i modelu w kontener
def putting_API_and_model_into_contener(**kwargs):
    print()


# Funkcja publikująca kontener
def contener_publication(**kwargs):
    print()


# Tworzenie DAG-a
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="6_contenerysation_and_api_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2020, 11, 1),
    catchup=False,
) as dag:

    # Task: Tworząca API pobierająca model
    task_creat_API = PythonOperator(
        task_id="creat_API",
        python_callable=creat_API,
        provide_context=True,
    )

    # Task: Opakowująca API i modelu w kontener
    task_putting_API_and_model_into_contener = PythonOperator(
        task_id="putting_API_and_model_into_contener",
        python_callable=putting_API_and_model_into_contener,
        provide_context=True,
    )

    # Task: Publikująca kontener
    task_contener_publication = PythonOperator(
        task_id="normalizing_and_standarizning",
        python_callable=contener_publication,
        provide_context=True,
    )

    # Ustawienie przebiegu tasków
    task_creat_API >> task_putting_API_and_model_into_contener >> contener_publication
