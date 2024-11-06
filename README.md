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
Posiada on:
- Patient_ID
- Wartości kategorialne:
  - Binarne:
    - Gender *(Male, Female)*
  - Inne:
    - Smoking_History *(Former Smoker, Current Smoker, Never Smoked)*
    - Tumor_Location *(Upper Lobe, Middle Lobe, Lower Lobe)*
    - Stage *(Stage IV, Stage III, Stage I, Stage II)*
    - **Treatment** *(Radiation Therapy, Surgery, Chemotherapy, Targeted Therapy)*
- Wartości liczbowe:
  - Age *(od 30 do 79)*
  - Tumor_Size_mm *(od 10 do 100)*
