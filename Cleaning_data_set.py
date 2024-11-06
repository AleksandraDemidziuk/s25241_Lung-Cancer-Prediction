import kagglehub
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Download latest version
path = kagglehub.dataset_download("rashadrmammadov/lung-cancer-prediction")
path += "\lung_cancer_data.csv"

df = pd.read_csv(path)
print(df.head())

if df.isnull().values.any():
    df.dropna(inplace=True)

numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
print(numeric_columns)

# Standaryzacja danych
scaler = StandardScaler()
df[numeric_columns] = pd.DataFrame(scaler.fit_transform(df[numeric_columns]), columns=numeric_columns, index=df.index)
print(df.head())
joblib.dump(scaler, 'Encoders/scaler.pkl')

# Kategoryzacja danych
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])
    joblib.dump(label_encoder, 'Encoders/label_encoder_{}.pkl'.format(column))
print(df.head())