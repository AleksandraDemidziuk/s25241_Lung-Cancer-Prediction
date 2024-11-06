# s25241_Lung-Cancer-Prediction

## Wprowadzenie
**Cel projektu** <br>
Celem projektu jest przewidzenie najlepszego sposobu leczenia na podstawie podanych informacji o pacjencie. Może to
pomóc lekarzom w wyborze sposobu leczenia i tym samym przyśpieszyć leczenie pacjenta.

### Informacje i opis zbioru danych danych
**Informacje o zbiorze danych** <br>
Zbiór danych nazwywa się [Lung Cancer Prediction](https://www.kaggle.com/datasets/rashadrmammadov/lung-cancer-prediction).
Wybrałam podany znbiór danych ze względu na to, że posiada kolumnę która określa sposób leczenia oraz jest dostępny do
użtku publicznego.

**Opis zbioru danych** <br>
Posiada on 38 kolumn:
- Patient_ID
- Wartości kategorialne:
  - Binarne:
    - Gender *(Male, Female)* <br>
      ![Gender distribution](Images/Columns/Gender.png)
    - Family_History *(Yes, No)* <br>
      ![Family_History distribution](Images/Columns/Family_History.png)
    - Comorbidity_Diabetes *(Yes, No)* <br>
      ![Comorbidity_Diabetes distribution](Images/Columns/Comorbidity_Diabetes.png)
    - Comorbidity_Hypertension *(Yes, No)* <br>
      ![Comorbidity_Hypertension distribution](Images/Columns/Comorbidity_Hypertension.png)
    - Comorbidity_Heart_Disease *(Yes, No)* <br>
      ![Comorbidity_Heart_Disease distribution](Images/Columns/Comorbidity_Heart_Disease.png)
    - Comorbidity_Chronic_Lung_Disease *(Yes, No)* <br>
      ![Comorbidity_Chronic_Lung_Disease distribution](Images/Columns/Comorbidity_Chronic_Lung_Disease.png)
    - Comorbidity_Kidney_Disease *(Yes, No)* <br>
      ![Comorbidity_Kidney_Disease distribution](Images/Columns/Comorbidity_Kidney_Disease.png)
    - Comorbidity_Autoimmune_Disease *(Yes, No)* <br>
      ![Comorbidity_Autoimmune_Disease distribution](Images/Columns/Comorbidity_Autoimmune_Disease.png)
    - Comorbidity_Other *(Yes, No)* <br>
      ![Comorbidity_Other distribution](Images/Columns/Comorbidity_Other.png)
  - Inne:
    - Smoking_History *(Former Smoker, Current Smoker, Never Smoked)* <br>
      ![Smoking_History](Images/Columns/Smoking_History.png)
    - Tumor_Location *(Upper Lobe, Middle Lobe, Lower Lobe)* <br>
      ![Tumor_Location distribution](Images/Columns/Tumor_Location.png)
    - Stage *(Stage IV, Stage III, Stage I, Stage II)* <br>
      ![Stage distribution](Images/Columns/Stage.png)
    - **Treatment** *(Radiation Therapy, Surgery, Chemotherapy, Targeted Therapy)* <br>
      ![Treatment distribution](Images/Columns/Treatment.png)
    - Ethnicity *(Caucasian, Hispanic, African American, Asian, Other)* <br>
      ![Ethnicity distribution](Images/Columns/Ethnicity.png)
    - Insurance_Type *(Medicare, Medicaid, Private, Other)* <br>
      ![Insurance_Type distribution](Images/Columns/Insurance_Type.png)
    - Performance_Status *(0, 1, 2, 3, 4)* <br>
      ![Performance_Status distribution](Images/Columns/Performance_Status.png)
- Wartości liczbowe:
  - Age *(od 30 do 79)* <br>
    ![Age distribution](Images/Columns/Age.png)
  - Tumor_Size_mm *(od 10 do 100)* <br>
    ![Tumor_Size_mm distribution](Images/Columns/Tumor_Size_mm.png)
  - Survival_Months *(od 1 do 119)* <br>
    ![Survival_Months distribution](Images/Columns/Survival_Months.png)
  - Blood_Pressure_Systolic *(od 90 do 179)* <br>
    ![Blood_Pressure_Systolic](Images/Columns/Blood_Pressure_Systolic.png)
  - Blood_Pressure_Diastolic *(od 60 do 109)* <br>
    ![Blood_Pressure_Diastolic distribution](Images/Columns/Blood_Pressure_Diastolic.png)
  - Blood_Pressure_Pulse *(od 60 do 99)* <br>
    ![Blood_Pressure_Pulse distribution](Images/Columns/Blood_Pressure_Pulse.png)
  - Hemoglobin_Level *(od 10 do 18)* <br>
    ![Hemoglobin_Level distribution](Images/Columns/Hemoglobin_Level.png)
  - White_Blood_Cell_Count *(od 3,5 do 10)* <br>
    ![White_Blood_Cell_Count distribution](Images/Columns/White_Blood_Cell_Count.png)
  - Platelet_Count *(od 150 d0 450)* <br>
    ![Platelet_Count distribution](Images/Columns/Platelet_Count.png)
  - Albumin_Level *(od 3 do 5)* <br>
    ![Albumin_Level distribution](Images/Columns/Albumin_Level.png)
  - Alkaline_Phosphatase_Level *(od 30 do 120)* <br>
    ![Alkaline_Phosphatase_Level distribution](Images/Columns/Alkaline_Phosphatase_Level.png)
  - Alanine_Aminotransferase_Level *(od 5 do 40)* <br>
    ![Alanine_Aminotransferase_Level distribution](Images/Columns/Alanine_Aminotransferase_Level.png)
  - Aspartate_Aminotransferase_Level *(od 10 do 50)* <br>
    ![Aspartate_Aminotransferase_Level distribution](Images/Columns/Aspartate_Aminotransferase_Level.png)
  - Creatinine_Level *(od 0,5 do 1,5)* <br>
    ![Creatinine_Level distribution](Images/Columns/Creatinine_Level.png)
  - LDH_Level *(od 100 do 250)* <br>
    ![LDH_Level distribution](Images/Columns/LDH_Level.png)
  - Calcium_Level *(od 6 do 10,5)* <br>
    ![Calcium_Level distribution](Images/Columns/Calcium_Level.png)
  - Phosphorus_Level *(od 2,5 do 5)* <br>
    ![Phosphorus_Level distribution](Images/Columns/Phosphorus_Level.png)
  - Glucose_Level *(od 70 do 150)* <br>
    ![Glucose_Level distribution](Images/Columns/Glucose_Level.png)
  - Potassium_Level *(od 3,5 do 5)* <br>
    ![Potassium_Level distribution](Images/Columns/Potassium_Level.png)
  - Sodium_Level *(od 135 do 145)* <br>
    ![Sodium_Level distribution](Images/Columns/Sodium_Level.png)
  - Smoking_Pack_Years *(0.02 do 100)* <br>
    ![Smoking_Pack_Years distribution](Images/Columns/Smoking_Pack_Years.png)

**Korelacje** <br>
Przy próbie znalezienia korelacji i przy sprawdzaniu danych zauważyłam, że dane są równo rozłożone co powoduje małą różnicę
i trudność w znalezieniu korelacji. <br>
![Korelacja 1?](Images/Corelations/Korelacje.png) <br>
![Korelacja 2?](Images/Corelations/Korelacje2.png) <br>
![Korelacja 3?](Images/Corelations/Korelacje3.png)

### Wygląd projektu
Projekt będzie przeprowadznony w poniższy sposób: <br>
![Diagram przepływu](Images/Diagram_przeplywu.png)
