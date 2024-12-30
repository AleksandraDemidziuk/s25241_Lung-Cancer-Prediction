import kagglehub
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Funkcja pobierająca dane
def download_data(**kwargs):
    # Czytanie danych
    path = kagglehub.dataset_download("rashadrmammadov/lung-cancer-prediction")
    path += "\lung_cancer_data.csv"
    df = pd.read_csv(path)

    # Przekazanie do następnego taska
    kwargs['ti'].xcom_push(key='data', value=df)

# Funkcja dzieląca dane
def split_data(**kwargs):
    # Pobranie danych z poprzedniego taska
    df = kwargs['ti'].xcom_pull(task_ids="download_data", key="data")

    # Podział danych
    train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)

    # Przekazanie do następnego taska
    kwargs['ti'].xcom_push(key='train_data', value=train_data)
    kwargs['ti'].xcom_push(key='test_data', value=test_data)


# Funkcja zapisująca dane do Google Sheets
def upload_to_gsheets(**kwargs):
    # Pobranie danych z poprzedniego taska
    ti = kwargs['ti']
    train_data = ti.xcom_pull(task_ids="split_data", key="train_data")
    test_data = ti.xcom_pull(task_ids="split_data", key="test_data")

    # Połączenie z Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/opt/Airflow/keys/lab-2-s25241-d848cad516a6.json', scope)
    client = gspread.authorize(creds)

    # Tworzenie nowych arkuszy i wgrywanie danych
    sheet_name = "ASI - Projekt 3"
    sheet = client.create(sheet_name)

    # Usuwanie arkuszy
    for worksheet in sheet.worksheets():
        if worksheet.title == "Zbiór modelowy" or worksheet.title == "Zbiór douczeniowy":
            sheet.del_worksheet(worksheet)

    # Dodanie arkuszy
    train_sheet = sheet.add_worksheet(title="Zbiór modelowy", rows=train_data.shape[0], cols=train_data.shape[1])
    test_sheet = sheet.add_worksheet(title="Zbiór douczeniowy", rows=test_data.shape[0], cols=test_data.shape[1])

    # Zapis danych
    train_sheet.update([train_data.columns.values.tolist()] + train_data.values.tolist())
    test_sheet.update([test_data.columns.values.tolist()] + test_data.values.tolist())


# Tworzenie DAG-a
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="3_download-public_split_save_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2020, 11, 1),
    catchup=False,
) as dag:

    # Task: Pobranie danych
    task_download_data = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
        provide_context=True,
    )

    # Task: Podział danych
    task_split_data = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
        provide_context=True,
    )

    # Task: Zapis do Google Sheets
    task_upload_to_gsheets = PythonOperator(
        task_id="upload_to_gsheets",
        python_callable=upload_to_gsheets,
        provide_context=True,
    )

    # Ustawienie przebiegu tasków
    task_download_data >> task_split_data >> task_upload_to_gsheets
