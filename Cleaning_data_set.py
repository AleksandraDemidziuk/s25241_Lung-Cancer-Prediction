import kagglehub
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Pobieranie danych
path = kagglehub.dataset_download("rashadrmammadov/lung-cancer-prediction")
path += "\lung_cancer_data.csv"

# Sprawdzenie informacji o danych
df = pd.read_csv(path)
print(df.head())
print(df.shape)

# Poprawienie danych
if df.isnull().values.any():
    df.dropna(inplace=True)
df.drop("Insurance_Type", axis=1, inplace=True)
df.drop("Patient_ID", axis=1, inplace=True)
df['Performance_Status'] = df['Performance_Status'].astype('category')

# Przygotowanie do standaryzacji i kategoryzacji
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_columns = df.select_dtypes(exclude=[np.number]).columns.tolist()
categorical_columns.remove('Treatment')

# Standaryzacja danych
scaler = StandardScaler()
df[numeric_columns] = pd.DataFrame(scaler.fit_transform(df[numeric_columns]), columns=numeric_columns, index=df.index)
print(df.head())
joblib.dump(scaler, 'Encoders/scaler.pkl')

# Kategoryzacja danych
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])
    joblib.dump(label_encoder, 'Encoders/label_encode{}.pkl'.format(column))

train, test = train_test_split(df, test_size=0.3)

# Zapisz do pliku CSV
train.to_csv("Data_sets/train_data.csv", index=False)
test.to_csv("Data_sets/test_data.csv", index=False)
