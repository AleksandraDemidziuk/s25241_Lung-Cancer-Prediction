# s25241_Lung-Cancer-Prediction


## Spis treści
- [Wprowadzenie](#wprowadzenie)
  - [Informacje i opis zbioru danych danych](#informacje-i-opis-zbioru-danych-danych)
  - [Wygląd projektu](#wygląd-projektu)
- [Efekty analizy danych](#efekty-analizy-danych)
  - [Własna](#własna)
  - [Automatyczna](#automatyczna)
    - [Aktualizacja](#aktualizacja)
  - [Podsumowanie analizy](#podsumowanie-analizy)
- [Modele](#modele)
  - [Bez zaokrąglenia danych](#bez-zaokrąglenia-danych)
  - [Z zaokrągleniem danych do 2 miejsca po przecinku](#z-zaokrągleniem-danych-do-2-miejsca-po-przecinku)
  - [Wybrany model](#wybrany-model)
- [Praca na daych i budowa modelu w Airflow](#praca-na-daych-i-budowa-modelu-w-airflow)
  - [Przygortowanie danych](#przygortowanie-danych)
  - [Przetwarzanie danych](#przetwarzanie-danych)
- [Jak uruchomić?](#jak-uruchomić)
  - [Jak uruchomić Airflow?](#jak-uruchomić-airflow)
  - [Jak uruchomić REST API?](#jak-uruchomić-rest-api)
  - [Jak testować API przez curl?](#jak-testować-api-przez-curl)
- [Sprawdzenie działania API](#sprawdzenie-działania-api)

## Wprowadzenie
**Cel projektu** <br>
&nbsp; Celem projektu jest przewidzenie najlepszego sposobu leczenia na podstawie podanych informacji o pacjencie. Może to
pomóc lekarzom w wyborze sposobu leczenia i tym samym przyśpieszyć leczenie pacjenta.

### Informacje i opis zbioru danych danych
**Informacje o zbiorze danych** <br>
&nbsp; Zbiór danych nazwywa się [Lung Cancer Prediction](https://www.kaggle.com/datasets/rashadrmammadov/lung-cancer-prediction).
Wybrałam podany znbiór danych ze względu na to, że posiada kolumnę która określa sposób leczenia oraz jest dostępny do
użtku publicznego.

**Opis zbioru danych** <br>
Posiada on 38 kolumn:
- Patient_ID {usunięta ze względu na bycie id wiersza}
- Wartości kategorialne:
  - Binarne:
    - Gender *(Male, Female)* <br>
      ![Gender distribution](Task_1_and_2/Images/First_analyzes/Distribution/Gender.png)
    - Family_History *(Yes, No)* <br>
      ![Family_History distribution](Task_1_and_2/Images/First_analyzes/Distribution/Family_History.png)
    - Comorbidity_Diabetes *(Yes, No)* <br>
      ![Comorbidity_Diabetes distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Diabetes.png)
    - Comorbidity_Hypertension *(Yes, No)* <br>
      ![Comorbidity_Hypertension distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Hypertension.png)
    - Comorbidity_Heart_Disease *(Yes, No)* <br>
      ![Comorbidity_Heart_Disease distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Heart_Disease.png)
    - Comorbidity_Chronic_Lung_Disease *(Yes, No)* <br>
      ![Comorbidity_Chronic_Lung_Disease distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Chronic_Lung_Disease.png)
    - Comorbidity_Kidney_Disease *(Yes, No)* <br>
      ![Comorbidity_Kidney_Disease distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Kidney_Disease.png)
    - Comorbidity_Autoimmune_Disease *(Yes, No)* <br>
      ![Comorbidity_Autoimmune_Disease distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Autoimmune_Disease.png)
    - Comorbidity_Other *(Yes, No)* <br>
      ![Comorbidity_Other distribution](Task_1_and_2/Images/First_analyzes/Distribution/Comorbidity_Other.png)
  - Inne:
    - Smoking_History *(Former Smoker, Current Smoker, Never Smoked)* <br>
      ![Smoking_History](Task_1_and_2/Images/First_analyzes/Distribution/Smoking_History.png)
    - Tumor_Location *(Upper Lobe, Middle Lobe, Lower Lobe)* <br>
      ![Tumor_Location distribution](Task_1_and_2/Images/First_analyzes/Distribution/Tumor_Location.png)
    - Stage *(Stage IV, Stage III, Stage I, Stage II)* <br>
      ![Stage distribution](Task_1_and_2/Images/First_analyzes/Distribution/Stage.png)
    - **Treatment** *(Radiation Therapy, Surgery, Chemotherapy, Targeted Therapy)* <br>
      ![Treatment distribution](Task_1_and_2/Images/First_analyzes/Distribution/Treatment.png)
    - Ethnicity *(Caucasian, Hispanic, African American, Asian, Other)* <br>
      ![Ethnicity distribution](Task_1_and_2/Images/First_analyzes/Distribution/Ethnicity.png)
    - Insurance_Type *(Medicare, Medicaid, Private, Other)* {usunięta ze względu różnicy w różnych krajach}<br>
      ![Insurance_Type distribution](Task_1_and_2/Images/First_analyzes/Distribution/Insurance_Type.png)
    - Performance_Status *(0, 1, 2, 3, 4)* <br>
      ![Performance_Status distribution](Task_1_and_2/Images/First_analyzes/Distribution/Performance_Status.png)
- Wartości liczbowe:
  - Age *(od 30 do 79)* <br>
    ![Age distribution](Task_1_and_2/Images/First_analyzes/Distribution/Age.png)
  - Tumor_Size_mm *(od 10 do 100)* <br>
    ![Tumor_Size_mm distribution](Task_1_and_2/Images/First_analyzes/Distribution/Tumor_Size_mm.png)
  - Survival_Months *(od 1 do 119)* <br>
    ![Survival_Months distribution](Task_1_and_2/Images/First_analyzes/Distribution/Survival_Months.png)
  - Blood_Pressure_Systolic *(od 90 do 179)* <br>
    ![Blood_Pressure_Systolic](Task_1_and_2/Images/First_analyzes/Distribution/Blood_Pressure_Systolic.png)
  - Blood_Pressure_Diastolic *(od 60 do 109)* <br>
    ![Blood_Pressure_Diastolic distribution](Task_1_and_2/Images/First_analyzes/Distribution/Blood_Pressure_Diastolic.png)
  - Blood_Pressure_Pulse *(od 60 do 99)* <br>
    ![Blood_Pressure_Pulse distribution](Task_1_and_2/Images/First_analyzes/Distribution/Blood_Pressure_Pulse.png)
  - Hemoglobin_Level *(od 10 do 18)* <br>
    ![Hemoglobin_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Hemoglobin_Level.png)
  - White_Blood_Cell_Count *(od 3,5 do 10)* <br>
    ![White_Blood_Cell_Count distribution](Task_1_and_2/Images/First_analyzes/Distribution/White_Blood_Cell_Count.png)
  - Platelet_Count *(od 150 d0 450)* <br>
    ![Platelet_Count distribution](Task_1_and_2/Images/First_analyzes/Distribution/Platelet_Count.png)
  - Albumin_Level *(od 3 do 5)* <br>
    ![Albumin_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Albumin_Level.png)
  - Alkaline_Phosphatase_Level *(od 30 do 120)* <br>
    ![Alkaline_Phosphatase_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Alkaline_Phosphatase_Level.png)
  - Alanine_Aminotransferase_Level *(od 5 do 40)* <br>
    ![Alanine_Aminotransferase_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Alanine_Aminotransferase_Level.png)
  - Aspartate_Aminotransferase_Level *(od 10 do 50)* <br>
    ![Aspartate_Aminotransferase_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Aspartate_Aminotransferase_Level.png)
  - Creatinine_Level *(od 0,5 do 1,5)* <br>
    ![Creatinine_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Creatinine_Level.png)
  - LDH_Level *(od 100 do 250)* <br>
    ![LDH_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/LDH_Level.png)
  - Calcium_Level *(od 6 do 10,5)* <br>
    ![Calcium_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Calcium_Level.png)
  - Phosphorus_Level *(od 2,5 do 5)* <br>
    ![Phosphorus_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Phosphorus_Level.png)
  - Glucose_Level *(od 70 do 150)* <br>
    ![Glucose_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Glucose_Level.png)
  - Potassium_Level *(od 3,5 do 5)* <br>
    ![Potassium_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Potassium_Level.png)
  - Sodium_Level *(od 135 do 145)* <br>
    ![Sodium_Level distribution](Task_1_and_2/Images/First_analyzes/Distribution/Sodium_Level.png)
  - Smoking_Pack_Years *(0.02 do 100)* <br>
    ![Smoking_Pack_Years distribution](Task_1_and_2/Images/First_analyzes/Distribution/Smoking_Pack_Years.png)

**Korelacje** <br>
Przy próbie znalezienia korelacji i przy sprawdzaniu danych zauważyłam, że dane są równo rozłożone co powoduje małą różnicę
i trudność w znalezieniu korelacji. <br>
![Korelacja 1?](Task_1_and_2/Images/First_analyzes/Corelations/Korelacje.png) <br>
![Korelacja 2?](Task_1_and_2/Images/First_analyzes/Corelations/Korelacje2.png) <br>
![Korelacja 3?](Task_1_and_2/Images/First_analyzes/Corelations/Korelacje3.png)

### Wygląd projektu
Projekt będzie przeprowadznony w poniższy sposób: <br>
![Diagram przepływu](Task_1_and_2/Images/Diagram_przeplywu.png)


## Efekty analizy danych
&nbsp; Dokładne efekty działania można zobaczyć w [Analizying_data_set.ipynb](Task_1_and_2/Analizying_data_set.ipynb).

### Własna
&nbsp; Jak można zobaczyć trzeba było zmienić kolumnę Performance_Status z numerycznej na kategorialną ponieważ ma konkretnie
5 różnych wartości (kategori) z których można wybrać wartość. Dalej można zobaczyć rozkład wartości każdej kolumn które
zostały przedstawione w formie wykresów. Można na nich zauważyć, że dane są dość równomiernie rozłożone. W dalszej części 
można też zauważyć wykresy pudełkowe dla wartości numerycznych które wydają się podobne do siebie. Można na nich zobaczyć,
że minimalna wartość, wartość w 1/4, wartość w połowie, wartość w 3/4 i wartość maksymalna są odpowiednio w podobnych odległościach.
Dalej jest przedstawiona tabela korelacji wartości numerycznych na której można zauważyć, że takich korelacji nie ma. Na
koniec zostało sprawdzone czy są jakieś wartości brakujące, ale ze względu na to, że takowych wartości nie ma to nic oprócz 
tego nie zostało wyświetlone.

### Automatyczna
&nbsp; Niestety analiza zautomatyzowanymi narzędziami okazała się niezbyt możliwa, ze względu na niekompatybilność, jak
i za dużą ilość danych przez które nie można było wygenerować wykresów. <br>
&nbsp; Efekty które udało się uzyskać to informacje o rodzaju danych w kolumnach, brakujących wartościach i rekomendacje
co do tego co można zrobić z danymi kolumnami. Jedynymi zmianami zaproponowanymi w czasie tej analizy było usunięcie kolumny
*Patient_ID*.

#### Aktualizacja
Udało się uruchomić Sweetviz po zmianie w pliku [***graph_numeric.py***](venv/Lib/site-packages/sweetviz/graph_numeric.py):
z:
``` python
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
# ...
warnings.filterwarnings('once', category=np.VisibleDeprecationWarning)
```
na:
``` python
warnings.filterwarnings('ignore', category=DeprecationWarning)
# ...
warnings.filterwarnings('once', category=DeprecationWarning)
```

Na początku sprawdziłam cały zbiór danych, a potem porównałam zbiór danych test i train. <br>

**Cały zbiór danych** <br>
Można zobaczyć brak korelacji i równomierne rozłożenie danych jak i czasami dużą różnorodność danych.
[Link do strony z wynikami](Task_1_and_2/Data_analyzes/sweetviz_report_full_data.html)<br>

**Porównanie zbioru danych test i train** <br>
Można zobaczyć, że procentowe rozłożenie danych jest dość wyrównane co powinno dobrze wpłynąć na trenowanie modelu.
[Link do stront z porównaniem](Task_1_and_2/Data_analyzes/sweetviz_report_test_train_comparison.html)


### Podsumowanie analizy
&nbsp; Podsumowując należy usunąć *Insurance_Type* i *Patient_ID*, pierwsze ze względu różnicy między krajami, a drugie
przez to, że jest to id co nie będzie potrzebne przy tworzeniu modelu. Dodatkowo nie widać pomiędzy między kolumnami korelacji,
więc trudno będzie wprowadzić jakieś zmiany związane z tym. Jednak można zauważyć wiele wartości które się nie powtarzają
przez co można pomyśleć czy nie warto jakoś ich zaokrąglić.

## Modele

### Bez zaokrąglenia danych
| Model | Wynik              | Jak został zrobiony                                                                                                                                                                                                                                                                                                                                                                                       | Inne informacje                                                                                                                                                  |
|----|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| #1 | 0.25638457265467657 | ExtraTreesClassifier(input_matrix, ExtraTreesClassifier__bootstrap=False, ExtraTreesClassifier__criterion=entropy, ExtraTreesClassifier__max_features=0.4, ExtraTreesClassifier__min_samples_leaf=15, ExtraTreesClassifier__min_samples_split=12, ExtraTreesClassifier__n_estimators=100)                                                                                                                 | {'generation': 5, 'mutation_count': 2, 'crossover_count': 0, 'predecessor': ('ExtraTreesClassifier(input_matrix, ExtraTreesClassifier__bootstrap=False, ExtraTreesClassifier__criterion=entropy, ExtraTreesClassifier__max_features=0.4, ExtraTreesClassifier__min_samples_leaf=5, ExtraTreesClassifier__min_samples_split=12, ExtraTreesClassifier__n_estimators=100)',), 'operator_count': 1, 'internal_cv_score': np.float64(0.25638457265467657)} |
| #2 | 0.25569309463296225 | KNeighborsClassifier(input_matrix, KNeighborsClassifier__n_neighbors=82, KNeighborsClassifier__p=2, KNeighborsClassifier__weights=uniform)                                                                                                                                                                                                                                                                | {'generation': 3, 'mutation_count': 1, 'crossover_count': 0, 'predecessor': ('KNeighborsClassifier(input_matrix, KNeighborsClassifier__n_neighbors=82, KNeighborsClassifier__p=2, KNeighborsClassifier__weights=distance)',), 'operator_count': 1, 'internal_cv_score': np.float64(0.25569309463296225)} |
| #3 | 0.25509031629399037 | KNeighborsClassifier(input_matrix, KNeighborsClassifier__n_neighbors=44, KNeighborsClassifier__p=1, KNeighborsClassifier__weights=uniform)                                                                                                                                                                                                                                                                | {'generation': 5, 'mutation_count': 1, 'crossover_count': 1, 'predecessor': ('BernoulliNB(input_matrix, BernoulliNB__alpha=100.0, BernoulliNB__fit_prior=True)',), 'operator_count': 1, 'internal_cv_score': np.float64(0.25509031629399037)} |
| #4 | 0.25500392339829914 | GradientBoostingClassifier(input_matrix, GradientBoostingClassifier__learning_rate=1.0, GradientBoostingClassifier__max_depth=9, GradientBoostingClassifier__max_features=0.4, GradientBoostingClassifier__min_samples_leaf=19, GradientBoostingClassifier__min_samples_split=3, GradientBoostingClassifier__n_estimators=100, GradientBoostingClassifier__subsample=0.6500000000000001)                  | {'generation': 0, 'mutation_count': 0, 'crossover_count': 0, 'predecessor': ('ROOT',), 'operator_count': 1, 'internal_cv_score': np.float64(0.25500392339829914)} |
| #5 | 0.2550036257483571 | GradientBoostingClassifier(input_matrix, GradientBoostingClassifier__learning_rate=0.01, GradientBoostingClassifier__max_depth=2, GradientBoostingClassifier__max_features=0.9000000000000001, GradientBoostingClassifier__min_samples_leaf=13, GradientBoostingClassifier__min_samples_split=2, GradientBoostingClassifier__n_estimators=100, GradientBoostingClassifier__subsample=0.7500000000000001)  | {'generation': 1, 'mutation_count': 1, 'crossover_count': 0, 'predecessor': ('BernoulliNB(input_matrix, BernoulliNB__alpha=100.0, BernoulliNB__fit_prior=False)',), 'operator_count': 1, 'internal_cv_score': np.float64(0.2550036257483571)} |

### Z zaokrągleniem danych do 2 miejsca po przecinku
| Model | Wynik              | Jak został zrobiony                                                                                                                                                                                                                                                                          | Inne informacje                                                                                                                                                                                                                                                                                                                                                                                                |
|----|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| #1 | 0.2585402279477669 | SGDClassifier(input_matrix, SGDClassifier__alpha=0.0, SGDClassifier__eta0=0.01, SGDClassifier__fit_intercept=True, SGDClassifier__l1_ratio=0.25, SGDClassifier__learning_rate=constant, SGDClassifier__loss=modified_huber, SGDClassifier__penalty=elasticnet, SGDClassifier__power_t=10.0)  | {'generation': 0, 'mutation_count': 0, 'crossover_count': 0, 'predecessor': ('ROOT',), 'operator_count': 1, 'internal_cv_score': np.float64(0.2585402279477669)}                                                                                                                                                                                                                                               |
| #2 | 0.2550028072110163 | DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=entropy, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=11, DecisionTreeClassifier__min_samples_split=5)                                            | {'generation': 4, 'mutation_count': 2, 'crossover_count': 0, 'predecessor': ('DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=entropy, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=19, DecisionTreeClassifier__min_samples_split=5)',), 'operator_count': 2, 'internal_cv_score': np.float64(0.2550028072110163)}  |
| #3 | 0.2547440005863704 | DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=gini, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=11, DecisionTreeClassifier__min_samples_split=5)                                               | {'generation': 5, 'mutation_count': 3, 'crossover_count': 0, 'predecessor': ('DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=entropy, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=11, DecisionTreeClassifier__min_samples_split=5)',), 'operator_count': 2, 'internal_cv_score': np.float64(0.2547440005863704)}  |
| #4 | 0.2545712892074735 | DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=entropy, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=5, DecisionTreeClassifier__min_samples_split=11)                                            | {'generation': 4, 'mutation_count': 3, 'crossover_count': 0, 'predecessor': ('DecisionTreeClassifier(RBFSampler(input_matrix, RBFSampler__gamma=0.2), DecisionTreeClassifier__criterion=entropy, DecisionTreeClassifier__max_depth=6, DecisionTreeClassifier__min_samples_leaf=19, DecisionTreeClassifier__min_samples_split=11)',), 'operator_count': 2, 'internal_cv_score': np.float64(0.2545712892074735)} |
| #5 | 0.2543125942015559 | KNeighborsClassifier(RobustScaler(input_matrix), KNeighborsClassifier__n_neighbors=15, KNeighborsClassifier__p=1, KNeighborsClassifier__weights=uniform)                                                                                                                                     | {'generation': 4, 'mutation_count': 2, 'crossover_count': 0, 'predecessor': ('BernoulliNB(RobustScaler(input_matrix), BernoulliNB__alpha=1.0, BernoulliNB__fit_prior=True)',), 'operator_count': 2, 'internal_cv_score': np.float64(0.2543125942015559)}                                                                                                                                                       |

### Wybrany model

Wybrałam model #1 z grupy działającej na zaokrąglonych danych, ponieważ daje najlepszy wynik.

**Wyniki modelu** <br>
Wyniki modelu: <br>
accuracy: 0.2457729468599034 <br>
precision: 0.2402012891721489 <br>
F1: 0.2190883897895028 <br>

## Praca na daych i budowa modelu w Airflow

Na początku zrobiłam dag testowy który potem próbowałam uruchomić co udało się wykonać. Kod który użyłam w tym dagu zalazłam
na stronie.

### Przygortowanie danych

Skrypt znajduje się w [DAG/3_download-public_split_save.py](DAG/3_download-public_split_save.py). <br>
Do tworzenia tego skrypty napoczątku uzyskałąm informację o tworzeniu dagów. Potem dostosowałam je do mojego problemu i
danych. Czego efektem są 3 funkcje i dag, a w nim 3 taski. Po zakończniu pisania zostały sprawdzone wcześniej dodane komentarze.

### Przetwarzanie danych

Skrypt znajduje się w [DAG/3_download-cloud_clean_standard-normalisate_save.py](DAG/3_download-cloud_clean_standard-normalisate_save.py). <br>
Ten skrypt został wykonany na podstawie *3_download-public_split_save.py* i *Cleaning_data_set.py*. Przez co praca nad nim
była łatwiejsza. Jak w przygotowaniu danych komentarze zostały sprawdzone i poprawione.

## Jak uruchomić?

### Jak uruchomić Airflow?
Pobierz projekt
```bash
git clone https://github.com/PJATK-ASI-2024/s25241_Lung-Cancer-Prediction.git
cd s25241_Lung-Cancer-Prediction/Airflow
```

Uruchomienie docker-compose **po raz pierwszy**:
``` bash
docker-compose up airflow-init
```
Uruchomienie docker-compose **po raz kolejny**:
``` bash
docker-compose up 
```

A następnie zaloguj się na stronie: <br>
Wejdź na http://localhost:8080 w przeglądarce.

Domyślne dane logowania: <br>
**Login**: airflow <br>
**Hasło**: airflow

Po wykonaniu podanych kroków wystarczy znaleźć dagi po id:
- 3_download-cloud_clean_standard-normalisate_save_dag
- 3_download-public_split_save_dag
- 4_building_model_dag
- 5_monitoring_dag
- 6_contenerysation_and_api_dag

### Jak uruchomić REST API?

Strona jest dostępna pod adresem http://127.0.0.1:5000/predict

#### Uruchomienie lokalne

``` bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

#### Uruchomienie przez obraz docker

Aby pobrać obraz z docker hub należy
``` bash
docker pull s25241/lung_cancer_prediction_api
```

Uruchomienie obrazu
``` bash
docker run -it s25241/lung_cancer_prediction_api "ścieżka_do_pliku"
```
**ścieżka_do_pliku ma być zamieniona na twoją własną.**

### Jak testować API przez curl?
**Pamiętaj żeby można było wykonać testy trzeba na początku zrobić [Jak uruchomić REST API?](#jak-uruchomić-rest-api).**
``` bash
 curl -X 'POST' 'http://127.0.0.1:5000/predict' -H 'accept: application/json' -H 'Content-Type: application/json' -d '@test_json.json'
```
Jeżeli nie macie własnych danych możecie przeprowadzić test przez użycie tych danych 
[Data_sets/test_json.json](test_json.json).


## Sprawdzenie działania API
Zostało ono sprawdzone na podaje stronie http://127.0.0.1:5000/docs#/default/predict_predict_post przez wklejenie zawartości
pliku [test_json.json](test_json.json).
