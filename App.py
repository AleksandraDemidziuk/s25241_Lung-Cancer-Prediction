from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Inicjalizacja aplikacji FastAPI
app = FastAPI()

# Załadowanie modelu
with open("Airflow/models/my_best_pipeline.pkl", "rb") as file:
    model = pickle.load(file)


# Definiowanie struktury danych wejściowych
class PredictionInput(BaseModel):
    Gender: str
    Family_History: str
    Comorbidity_Diabetes: str
    Comorbidity_Hypertension: str
    Comorbidity_Heart_Disease: str
    Comorbidity_Chronic_Lung_Disease: str
    Comorbidity_Kidney_Disease: str
    Comorbidity_Autoimmune_Disease: str
    Comorbidity_Other: str
    Smoking_History: str
    Tumor_Location: str
    Stage: str
    Ethnicity: str
    Insurance_Type:  str
    Performance_Status: int
    Age: int
    Tumor_Size_mm: float
    Survival_Months: int
    Blood_Pressure_Systolic: int
    Blood_Pressure_Diastolic: int
    Blood_Pressure_Pulse: int
    Hemoglobin_Level: float
    White_Blood_Cell_Count: float
    Platelet_Count: float
    Albumin_Level: float
    Alkaline_Phosphatase_Level: float
    Alanine_Aminotransferase_Level: float
    Aspartate_Aminotransferase_Level: float
    Creatinine_Level: float
    LDH_Level: float
    Calcium_Level: float
    Phosphorus_Level: float
    Glucose_Level: float
    Potassium_Level: float
    Sodium_Level: float
    Smoking_Pack_Years: float


# Endpoint do przewidywania
@app.post("/predict")
def predict(input_data: PredictionInput):
    # Przygotowanie danych do modelu
    data = np.array([[input_data.Gender, input_data.Family_History, input_data.Comorbidity_Diabetes,
                      input_data.Comorbidity_Hypertension, input_data.Comorbidity_Heart_Disease,
                      input_data.Comorbidity_Chronic_Lung_Disease, input_data.Comorbidity_Kidney_Disease,
                      input_data.Comorbidity_Autoimmune_Disease, input_data.Comorbidity_Other,
                      input_data.Smoking_History, input_data.Tumor_Location, input_data.Stage, input_data.Ethnicity,
                      input_data.Insurance_Type, input_data.Performance_Status, input_data.Age, input_data.Tumor_Size_mm,
                      input_data.Survival_Months, input_data.Blood_Pressure_Systolic, input_data.Blood_Pressure_Diastolic,
                      input_data.Blood_Pressure_Pulse, input_data.Hemoglobin_Level, input_data.White_Blood_Cell_Count,
                      input_data.Platelet_Count, input_data.Albumin_Level, input_data.Alkaline_Phosphatase_Level,
                      input_data.Alanine_Aminotransferase_Level, input_data.Aspartate_Aminotransferase_Level,
                      input_data.Creatinine_Level, input_data.LDH_Level, input_data.Calcium_Level,
                      input_data.Phosphorus_Level, input_data.Glucose_Level, input_data.Potassium_Level,
                      input_data.Sodium_Level, input_data.Smoking_Pack_Years]])

    # Przewidywanie
    prediction = model.predict(data)[0]

    # Zwrócenie wyniku jako JSON
    return {"Treatment": prediction}