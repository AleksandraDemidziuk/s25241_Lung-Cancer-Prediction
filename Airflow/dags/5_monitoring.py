from airflow.utils.email import send_email
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from pycaret.classification import *
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import numpy as np
from airflow.operators.dummy_operator import DummyOperator


# Funkcja pobierająca dane do Google Sheets
def get_model_and_data_from_gsheets(**kwargs):
    # Połączenie z Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/opt/Airflow/keys/lab-2-s25241-d848cad516a6.json', scope)
    client = gspread.authorize(creds)

    # Otworzenie arkusza
    sheet = client.open("ASI - Projekt 3")

    # Popranie konkretnego pod arkusza
    train_sheet = sheet.worksheet("Zbiór douczeniowy")

    # Pobranie danych z arkusza
    train_data = pd.DataFrame(train_sheet.get_all_records())

    # Pobranie modelu
    loaded_model = load_model('Airflow/models/my_best_pipeline')

    # Przekazanie danych dalej
    kwargs['ti'].xcom_push(key='data', value=train_data)
    kwargs['ti'].xcom_push(key='model', value=loaded_model)


# Walidacja modelu
def model_validation(**kwargs):
    # Pobranie danych z poprzedniego taska
    df = kwargs['ti'].xcom_pull(task_ids="get_model_and_data_from_gsheets", key="data")
    model = kwargs['ti'].xcom_pull(task_ids="get_model_and_data_from_gsheets", key="model")

    # Testowanie
    predictions = predict_model(model, data=df, raw_score=True)

    # Dodawanie informacji
    mail_info = ("Wyniki walidacji modelu:\n"
                 f"Accuracy = {predictions['Accuracy'].iloc[0]}, zaliczony = ")
    if predictions['Accuracy'] >= 0.25:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"AUC = {predictions['AUC'].iloc[0]}, zaliczony = "
    if predictions['AUC'] >= 0.49:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"Recall = {predictions['Recall'].iloc[0]}, zaliczony = "
    if predictions['Recall'] >= 0.25:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"Prec. = {predictions['Prec.'].iloc[0]}, zaliczony = "
    if predictions['Prec.'] >= 0.24:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"F1 = {predictions['F1'].iloc[0]}, zaliczony = "
    if predictions['F1'] >= 0.24:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"Kappa = {predictions['Kappa'].iloc[0]}, zaliczony = "
    if predictions['Kappa'] >= -0.01:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += f"MCC = {predictions['MCC'].iloc[0]}, zaliczony = "
    if predictions['MCC'] >= -0.01:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    # Przekazywanie danych dalej
    kwargs['ti'].xcom_push(key='mail_info', value=mail_info)


# Testowanie modelu na brak danych
def model_testing_missing_values(**kwargs):
    # Pobranie danych z poprzedniego taska
    df = kwargs['ti'].xcom_pull(task_ids="get_model_and_data_from_gsheets", key="data")
    model = kwargs['ti'].xcom_pull(task_ids="get_model_and_data_from_gsheets", key="model")
    mail_info = kwargs['ti'].xcom_pull(task_ids="model_validation", key="mail_info")

    # Przygotowanie danych
    probability = 0.2

    # Tworzenie maski losowej
    mask = np.random.rand(*df.shape) < probability
    df_with_nan = df.mask(mask)

    # Przeprowadzenie testu
    try:
        predictions = predict_model(model, data=df_with_nan, raw_score=True)
        mail_info += ("\nModel działa z barkującymi danymi.\n"
                      f"Otrzymane Accuracy to {predictions['Accuracy'].iloc[0]}")
    except Exception as e:
        mail_info += "\nModel nie działa z barkującymi danymi!!!"
    finally:
        # Przekazywanie danych dalej
        kwargs['ti'].xcom_push(key='mail_info', value=mail_info)


# Wysyłanie maila
def sending_mail(**kwargs):
    # Pobranie danych z poprzedniego taska
    body = kwargs['ti'].xcom_pull(task_ids="model_testing_missing_values", key="mail_info")

    subject = f"Monitorowanie i walidacja modelu"
    send_email(
        to='s25241@pjwstk.edu.pl',
        subject=subject,
        html_content=body,
    )


# Tworzenie DAG-a
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    'email_on_failure': True,
    'email_on_retry': True,
}

with DAG(
    dag_id="5_monitoring_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2020, 11, 1),
    catchup=False,
) as dag:

    # Task: Pobranie danych z Google sheets i modelu
    task_download_data = PythonOperator(
        task_id="download_data",
        python_callable=get_model_and_data_from_gsheets,
        provide_context=True,
    )

    # Task: Walidacja modelu
    model_validation = PythonOperator(
        task_id="model_validation",
        python_callable=model_validation,
        provide_context=True,
    )

    # Task: Sprawdzenie czy jest wstanie przewidywać z brakującymi wartościami
    model_testing_missing_values = PythonOperator(
        task_id="model_testing_missing_values",
        python_callable=model_testing_missing_values,
        provide_context=True,
    )

    # Task: Wysyłanie maila
    sending_mail = DummyOperator(
        task_id='seding_mail',
        on_success_callback=sending_mail,
        on_failure_callback=sending_mail,
        dag=dag,
    )

    # Ustawienie przebiegu tasków
    task_download_data >> model_validation >> model_testing_missing_values >> sending_mail
