from fastapi import FastAPI
from pycaret.classification import load_model, predict_model
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pandas as pd

# Inicjalizacja aplikacji FastAPI
app = FastAPI()

# Załadowanie modelu
model = load_model("Airflow/models/my_best_pipeline")


# Obsługa błędów
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"},
    )


# Definiowanie struktury danych wejściowych
class PredictionInput(BaseModel):
    Patient_ID: str
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
    input_df = pd.DataFrame([dict(input_data)])

    # Przewidywanie
    prediction = predict_model(model, data=input_df)['prediction_label'].values[0]

    # Zwrócenie wyniku jako JSON
    return {"Treatment": prediction}
