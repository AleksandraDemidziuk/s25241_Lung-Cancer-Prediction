FROM ubuntu:latest
LABEL authors="olenk"

# Ustalamy katalog roboczy
WORKDIR /app

# Kopiujemy plik z zależnościami do kontenera
COPY requirements_for_docker.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements_for_docker.txt

# Kopiujemy całą aplikację do kontenera
COPY Airflow/models /app/models/
COPY Airflow/App.py /app/

# Ustawiamy zmienną środowiskową
ENV PYTHONUNBUFFERED 1

# Uruchomienie serwera FastAPI na porcie 5000
CMD ["uvicorn", "App:app", "--host", "0.0.0.0", "--port", "5000"]