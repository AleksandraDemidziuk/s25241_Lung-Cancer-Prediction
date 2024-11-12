import joblib
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, accuracy_score, precision_score, f1_score
import os


script_dir = os.path.dirname(__file__)  # katalog, w którym jest skrypt
data_path = os.path.join(script_dir, "../Data_sets/train_data.csv")
df = pd.read_csv(data_path)

train, test = train_test_split(df, test_size=0.3)
x_train = train.loc[:, train.columns != "Treatment"]
y_train = train["Treatment"]
x_test = test.loc[:, train.columns != "Treatment"]
y_test = test["Treatment"]


model = SGDClassifier(alpha=0.0, eta0=0.01, fit_intercept=True, l1_ratio=0.25, learning_rate='constant', loss='modified_huber',
                      penalty='elasticnet', power_t=10.0)

model.fit(x_train, y_train)
predictions = model.predict(x_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')
F1 = f1_score(y_test, predictions, average='weighted')
#RMSE = root_mean_squared_error(y_test, predictions)
print(f"Wyniki modelu:\n"
      f"accuracy: {accuracy}\n"
      f"precision: {precision}\n"
      f"F1: {F1}\n")

joblib.dump(model, 'chosen_model.pkl')
