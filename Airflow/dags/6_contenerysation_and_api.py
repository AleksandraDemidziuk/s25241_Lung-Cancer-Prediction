from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import subprocess


# Funkcja tworząca API pobierająca model
def creat_API():
    print("Skryp tworzący API zanjduje się pod nazwą 'App.py'.")


# Funkcja opakowująca API i modelu w kontener
def putting_API_and_model_into_contener():
    try:
        # Tworzenie obrazu
        dockerfile_path = "Airflow/Thinks_for_task_6/Dockerfile"
        context_path = "Airflow/Thinks_for_task_6"
        subprocess.run(["docker", "build", "-t", "s25241/lung_cancer_prediction_api", "-f", dockerfile_path, context_path], check=True)
        print("Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")


# Funkcja publikująca kontener
def contener_publication():
    try:
        # Logowanie się do dockera
        subprocess.run(["docker", "login"], check=True)

        # Publikacja obrazu
        subprocess.run(["docker", "push", "s25241/lung_cancer_prediction_api"], check=True)

        print(f"Docker image pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


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
        task_id="contener_publication",
        python_callable=contener_publication,
        provide_context=True,
    )

    # Ustawienie przebiegu tasków
    task_creat_API >> task_putting_API_and_model_into_contener >> contener_publication
