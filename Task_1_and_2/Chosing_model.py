from tpot import TPOTClassifier
import pandas as pd
from sklearn.model_selection import train_test_split


# Pobranie danych i ich przygotowanie
df = pd.read_csv("Data_sets/train_data.csv")

train, test = train_test_split(df, test_size=0.3)
x_train = train.loc[:, train.columns != "Treatment"]
y_train = train["Treatment"]
x_test = test.loc[:, train.columns != "Treatment"]
y_test = test["Treatment"]

# Ustawienie AutoML
random_state = 62
tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2, random_state=random_state)
tpot.fit(x_train, y_train)

# Wybranie wybraniej liczby modeli
evaluated_individuals = tpot.evaluated_individuals_
sorted_models = sorted(evaluated_individuals.items(), key=lambda x: x[1]['internal_cv_score'], reverse=True)
top_5_models = sorted_models[:5]

# Eksport i ocena modeli
for i, (model_name, model_info) in enumerate(top_5_models):
    print(f"\nModel #{i + 1}: {model_name}")
    print(f"Score: {model_info['internal_cv_score']}")
    print(f"Other information about model: \n {model_info}")
