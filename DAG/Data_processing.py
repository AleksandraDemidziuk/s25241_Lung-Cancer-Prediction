import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# Funkcja pobierająca dane do Google Sheets
def get_from_gsheets(**kwargs):
    # Połączenie z Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('"C:/Users/olenk/OneDrive/Pulpit/Szkoła/Semestr 7/ASI/Lab_2/lab-2-s25241-d848cad516a6.json"', scope)
    client = gspread.authorize(creds)

    # Otworzenie arkusza
    sheet = client.open("ASI - Projekt 3")

    # Popranie konkretnego pod arkusza
    train_sheet = sheet.worksheet("Zbiór modelowy")

    # Pobranie danych z arkusza
    train_data = pd.DataFrame(train_sheet.get_all_records())

    # Przekazanie danych dalej
    kwargs['train_data'].xcom_push(key='train_data', value=train_data)


# Funkcja czyszcząca dane
def cleaning_data(**kwargs):
    # Pobieranie danych z poprzedniego zadania
    train_data = kwargs['train_data'].xcom_pull(task_ids="get_data_gsheets", key="train_data")

    # Czyszczenie danych
    if train_data.isnull().values.any():
        train_data.dropna(inplace=True)

    # Usuwanie duplikatów
    train_data_no_duplicates = train_data.drop_duplicates()

    # Przekazanie danych do następnego taska
    kwargs['cleans_train_data'].xcom_push(key='cleans_train_data', value=train_data_no_duplicates)


# Funkcja normalizująca i standaryzująca dane
def normalizing_and_standarizning(**kwargs):
    # Pobieranie danych z poprzedniego taska
    train_data = kwargs['cleans_train_data'].xcom_pull(task_ids="cleaning_data", key="cleans_train_data")

    # Przygotowanie do standaryzacji i kategoryzacji
    train_data['Performance_Status'] = train_data['Performance_Status'].astype('category')
    numeric_columns = train_data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = train_data.select_dtypes(exclude=[np.number]).columns.tolist()

    # Zaokrąglenie danych
    columns = ['Tumor_Size_mm', 'Hemoglobin_Level', 'White_Blood_Cell_Count', 'Platelet_Count', 'Albumin_Level',
               'Alkaline_Phosphatase_Level', 'Alanine_Aminotransferase_Level', 'Aspartate_Aminotransferase_Level',
               'Creatinine_Level', 'LDH_Level', 'Calcium_Level', 'Phosphorus_Level', 'Glucose_Level', 'Potassium_Level',
               'Sodium_Level', 'Smoking_Pack_Years']
    train_data[columns] = train_data[columns].round(2)

    # Standaryzacja danych
    scaler = StandardScaler()
    train_data[numeric_columns] = pd.DataFrame(scaler.fit_transform(train_data[numeric_columns]), columns=numeric_columns,
                                       index=train_data.index)

    # Kategoryzacja danych
    label_encoder = LabelEncoder()
    for column in categorical_columns:
        train_data[column] = label_encoder.fit_transform(train_data[column])

    # Przekazanie danych do następnego taska
    kwargs['normalized_train_data'].xcom_push(key='normalized_train_data', value=train_data)


# Funkcja zapisująca dane do Google Sheets
def upload_to_gsheets(**kwargs):
    # Pobranie danych z poprzedniego taska
    train_data = kwargs['normalized_train_data'].xcom_pull(task_ids="normalizing_and_standarizning",
                                                           key="normalized_train_datanormalized_train_data")

    # Połączenie z Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('"C:/Users/olenk/OneDrive/Pulpit/Szkoła/Semestr 7/ASI/Lab_2/lab-2-s25241-d848cad516a6.json"', scope)
    client = gspread.authorize(creds)

    # Otworzenie arkusza
    sheet = client.open("ASI - Projekt 3")

    # Dodanie arkuszy
    for worksheet in sheet.worksheets():
        if worksheet.title == "Przetworzony zbiór modelowy":
            sheet.del_worksheet(worksheet)
    train_sheet = sheet.add_worksheet(title="Przetworzony zbiór modelowy", rows=train_data.shape[0], cols=train_data.shape[1])

    # Zapis danych w google sheets
    train_sheet.update([train_data.columns.values.tolist()] + train_data.values.tolist())


# Tworzenie DAG-a
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="data_processing_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    # Task: Pobranie danych z Google sheets
    task_get_data_from_google_sheets = PythonOperator(
        task_id="getting_data",
        python_callable=get_from_gsheets,
        provide_context=True,
    )

    # Task: Czyszczenie danych
    task_cleaning_data = PythonOperator(
        task_id="cleaning_data",
        python_callable=cleaning_data,
        provide_context=True,
    )

    # Task: Normalizacja i standaryzacja danych
    task_normalizing_and_standarizning = PythonOperator(
        task_id="normalizing_and_standarizning",
        python_callable=normalizing_and_standarizning,
        provide_context=True,
    )

    # Task: Zapis do Google Sheets
    task_upload_to_gsheets = PythonOperator(
        task_id="upload_to_gsheets",
        python_callable=upload_to_gsheets,
        provide_context=True,
    )

    # Ustawienie przebiegu tasków
    task_get_data_from_google_sheets >> task_cleaning_data >> task_normalizing_and_standarizning >> task_upload_to_gsheets
