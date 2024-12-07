import json
import os
def zbierz_dane():
    dane = []

    for i in range(2):
        temperatura = float(input(f'Podaj temperaturę (w °C) dla pomiaru {i + 1}: '))
        cisnienie = float(input(f'Podaj ciśnienie (w hPa) dla pomiaru {i + 1}: '))

        pomiar = {
            'temperature': temperatura,
            'pressure': cisnienie
        }

        dane.append(pomiar)

    return dane

def zapisz_do_json(dane, nazwa_pliku):
    # Sprawdzenie, czy plik już istnieje
    plik_istnieje = os.path.exists(nazwa_pliku)

    with open(nazwa_pliku, 'a') as plik:
        if plik_istnieje:
            # Jeśli plik istnieje, dodaj przecinek przed nowymi danymi
            plik.write(',\n')
        else:
            # Jeśli plik nie istnieje, otwórz go w trybie zapisu i dodaj nawiasy
            plik.write('[\n')

        # Zapisz dane w formacie JSON
        json.dump(dane, plik, indent=4)

    # Zamknij nawiasy w pliku
    with open(nazwa_pliku, 'a') as plik:
        plik.write('\n]')

if __name__ == "__main__":
    dane = zbierz_dane()
    zapisz_do_json(dane, 'pomiary.json')
    print("Dane zostały zapisane w pliku pomiary.json")