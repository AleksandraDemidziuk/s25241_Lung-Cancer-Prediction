from fastapi import FastAPI
from pycaret.classification import load_model
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
@app.post("/predict")
async def predict(input_data: dict):
    try:
        # Przetwarzanie danych
        prediction = model.predict([input_data])
        return {"prediction": prediction[0]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


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
    input_df = pd.DataFrame([{"Patient_ID": input_data.Patient_ID, "Gender": input_data.Gender, "Family_History": input_data.Family_History,
                              "Comorbidity_Diabetes": input_data.Comorbidity_Diabetes, "Comorbidity_Hypertension": input_data.Comorbidity_Hypertension,
                              "Comorbidity_Heart_Disease": input_data.Comorbidity_Heart_Disease,
                              "Comorbidity_Chronic_Lung_Disease": input_data.Comorbidity_Chronic_Lung_Disease,
                              "Comorbidity_Kidney_Disease": input_data.Comorbidity_Kidney_Disease,
                              "Comorbidity_Autoimmune_Disease": input_data.Comorbidity_Autoimmune_Disease,
                              "Comorbidity_Other": input_data.Comorbidity_Other, "Smoking_History": input_data.Smoking_History,
                              "Tumor_Location": input_data.Tumor_Location, "Stage": input_data.Stage, "Ethnicity": input_data.Ethnicity,
                              "Insurance_Type": input_data.Insurance_Type, "Performance_Status": input_data.Performance_Status,
                              "Age": input_data.Age, "Tumor_Size_mm": input_data.Tumor_Size_mm, "Survival_Months": input_data.Survival_Months,
                              "Blood_Pressure_Systolic": input_data.Blood_Pressure_Systolic, "Blood_Pressure_Diastolic": input_data.Blood_Pressure_Diastolic,
                              "Blood_Pressure_Pulse": input_data.Blood_Pressure_Pulse, "Hemoglobin_Level": input_data.Hemoglobin_Level,
                              "White_Blood_Cell_Count": input_data.White_Blood_Cell_Count, "Platelet_Count": input_data.Platelet_Count,
                              "Albumin_Level": input_data.Albumin_Level, "Alkaline_Phosphatase_Level": input_data.Alkaline_Phosphatase_Level,
                              "Alanine_Aminotransferase_Level": input_data.Alanine_Aminotransferase_Level,
                              "Aspartate_Aminotransferase_Level": input_data.Aspartate_Aminotransferase_Level,
                              "Creatinine_Level": input_data.Creatinine_Level, "LDH_Level": input_data.LDH_Level,
                              "Calcium_Level": input_data.Calcium_Level, "Phosphorus_Level": input_data.Phosphorus_Level,
                              "Glucose_Level": input_data.Glucose_Level, "Potassium_Level": input_data.Potassium_Level,
                              "Sodium_Level": input_data.Sodium_Level, "Smoking_Pack_Years": input_data.Smoking_Pack_Years
                              }])

    # Przewidywanie
    prediction = model.predict(input_df)

    # Zwrócenie wyniku jako JSON
    return {"Treatment": prediction}
