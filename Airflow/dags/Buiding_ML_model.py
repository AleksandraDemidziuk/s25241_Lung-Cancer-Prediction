from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from sklearn.model_selection import train_test_split
from pycaret.datasets import get_data
from pycaret.classification import *
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


# Funkcja pobierająca dane do Google Sheets
def get_from_gsheets(**kwargs):
    # Połączenie z Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/opt/Airflow/keys/lab-2-s25241-d848cad516a6.json', scope)
    client = gspread.authorize(creds)

    # Otworzenie arkusza
    sheet = client.open("ASI - Projekt 3")

    # Popranie konkretnego pod arkusza
    train_sheet = sheet.worksheet("Przetworzony zbiór modelowy")

    # Pobranie danych z arkusza
    train_data = pd.DataFrame(train_sheet.get_all_records())

    # Przekazanie danych dalej
    kwargs['ti'].xcom_push(key='data', value=train_data)


# Funkcja dzieląca dane
def split_data(**kwargs):
    # Pobranie danych z poprzedniego taska
    df = kwargs['ti'].xcom_pull(task_ids="download_data", key="data")

    # Podział danych
    train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)

    # Przekazanie do następnego taska
    kwargs['ti'].xcom_push(key='train_data', value=train_data)
    kwargs['ti'].xcom_push(key='test_data', value=test_data)


def choosing_and_saving_model(**kwargs):
    train_data = kwargs['ti'].xcom_pull(key='train_data')
    test_data = kwargs['ti'].xcom_pull(key='test_data')

    # Załadowanie i pryzgotowanie data setu
    data = train_data
    s = setup(data, target='Treatment')

    # Sprawdzanie modeli
    best = compare_models()
    print(best)
    evaluate_model(best)
    if hasattr(best, 'predict_proba'):
        plot_model(best, plot='auc')
    
    plot_model(best, plot='confusion_matrix')
    predict_model(best)

    #
    predictions = predict_model(best, data=test_data, raw_score=True)
    predictions.head()

    save_model(best, 'Airflow/models/my_best_pipeline')


# Tworzenie DAG-a
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="building_ML_model_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2020, 11, 1),
    catchup=False,
) as dag:

    # Task: Pobranie danych z Google sheets
    task_download_data = PythonOperator(
        task_id="download_data",
        python_callable=get_from_gsheets,
        provide_context=True,
    )

    # Task: Podział danych
    task_split_data = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
        provide_context=True,
    )

    # Task: Wybranie i zapisanie najlepszego modelu
    task_choose_and_save_model = PythonOperator(
        task_id="upload_to_gsheets",
        python_callable=choosing_and_saving_model,
        provide_context=True,
    )

    # Ustawienie przebiegu tasków
    task_download_data >> task_split_data >> task_choose_and_save_model
