import adafruit_dht
import board
import json
import os
import time

# Konfiguracja
DHT_PIN = board.D4  # Pin GPIO (np. GPIO4 na Raspberry Pi)
DATA_FILE = "sensor_data.json"  # Nazwa pliku JSON do zapisu danych

# Inicjalizacja czujnika
dht_sensor = adafruit_dht.DHT11(DHT_PIN)


def read_sensor():
    """
    Odczytuje dane z czujnika DHT11.
    """
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        if humidity is not None and temperature is not None:
            return {"temperature": round(temperature, 1), "humidity": round(humidity, 1)}
        else:
            return None
    except RuntimeError as error:
        # Ignorujemy tymczasowe błędy odczytu
        print(f"Błąd odczytu: {error.args[0]}")
        return None


def save_to_json(data):
    """
    Zapisuje dane do pliku JSON.
    """
    try:
        existing_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                existing_data = json.load(file)
    except json.JSONDecodeError:
        pass

    # Dodaj nowe dane do istniejącej listy
    existing_data.append(data)

    with open(DATA_FILE, "w") as file:
        json.dump(existing_data, file, indent=4)


if __name__ == "__main__":
    while True:
        sensor_data = read_sensor()
        if sensor_data:
            sensor_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")  # Dodanie znaczniku czasu
            save_to_json(sensor_data)
            print(f"Dane zapisane: {sensor_data}")
        else:
            print("Błąd odczytu z czujnika. Sprawdź połączenia lub warunki środowiskowe.")

        # Przerwa między odczytami (np. co 10 sekund)
        time.sleep(10)
