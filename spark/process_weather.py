import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime

def main():
    spark = SparkSession.builder \
        .appName("Weather Data Processing") \
        .master("local[*]") \
        .getOrCreate()

    # Przykładowe dane JSON (symulacja odpowiedzi API)
    sample_json = """
    {
      "name": "Warsaw",
      "dt": 1685107200,
      "main": {
        "temp": 20.5,
        "humidity": 65,
        "pressure": 1012
      },
      "weather": [
        {
          "description": "clear sky"
        }
      ]
    }
    """

    # Załaduj JSON do Pythona (słownik)
    data = json.loads(sample_json)

    # Zamieniamy słownik na listę jednowierszową dla Spark
    rows = [(
        data["name"],
        data["dt"],
        data["main"]["temp"],
        data["main"]["humidity"],
        data["main"]["pressure"],
        data["weather"][0]["description"]
    )]

    # Definiujemy kolumny DataFrame
    columns = ["city", "timestamp", "temperature", "humidity", "pressure", "description"]

    # Tworzymy DataFrame
    df = spark.createDataFrame(rows, schema=columns)

    # Konwersja timestamp (unix) na czytelny format
    df = df.withColumn("datetime", from_unixtime(col("timestamp")))

    # Pokaż wynik
    df.select("city", "datetime", "temperature", "humidity", "pressure", "description").show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
