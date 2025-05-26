FROM bitnami/spark:latest

USER root

# Kopiuj skrypt PySpark do kontenera
COPY process_weather.py /opt/spark/app/process_weather.py

WORKDIR /opt/spark/app

# Domyślny CMD do uruchomienia skryptu
CMD ["spark-submit", "process_weather.py"]
