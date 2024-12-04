from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from pycaret.classification import *
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


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
                 "Accuracy = {}, zaliczony = ".format(predictions['Accuracy']))
    if predictions['Accuracy'] >= 0.25:
        mail_info += "tak\n"
    else:
        mail_info += "nie\n"

    mail_info += "AUC = {}, zaliczony = ".format(predictions['AUC'])
    if predictions['AUC'] >= 0.49:
        mail_info += "tak"
    else:
        mail_info += "nie"

    mail_info += "Recall = {}, zaliczony = ".format(predictions['Recall'])
    if predictions['Recall'] >= 0.25:
        mail_info += "tak"
    else:
        mail_info += "nie"

    mail_info += "Prec. = {}, zaliczony = ".format(predictions['Prec.'])
    if predictions['Prec.'] >= 0.24:
        mail_info += "tak"
    else:
        mail_info += "nie"

    mail_info += "F1 = {}, zaliczony = ".format(predictions['F1'])
    if predictions['F1'] >= 0.24:
        mail_info += "tak"
    else:
        mail_info += "nie"

    mail_info += "Kappa = {}, zaliczony = ".format(predictions['Kappa'])
    if predictions['Kappa'] >= -0.01:
        mail_info += "tak"
    else:
        mail_info += "nie"

    mail_info += "MCC = {}, zaliczony = ".format(predictions['MCC'])
    if predictions['MCC'] >= -0.01:
        mail_info += "tak"
    else:
        mail_info += "nie"

    # Przekazywanie danych dalej
    kwargs['ti'].xcom_push(key='mail_info', value=mail_info)
