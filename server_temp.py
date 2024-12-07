from bottle import route, run, request, static_file
import json
import os
import plotly.graph_objects as go

DATA_FILE = "pomiary.json"

# Funkcja do zapisu danych do pliku JSON
def save_data(temperature, pressure):
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass

    data.append({"temperature": temperature, "pressure": pressure})
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Funkcja do generowania wykresu w HTML
def generate_plot():
    if not os.path.exists(DATA_FILE):
        return "<h3>Brak danych do wyświetlenia</h3>"

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return "<h3>Brak danych do wyświetlenia</h3>"

    temperatures = [entry["temperature"] for entry in data]
    pressures = [entry["pressure"] for entry in data]
    indices = list(range(1, len(data) + 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=indices, y=temperatures, mode="lines+markers", name="Temperatura (°C)"))
    fig.add_trace(go.Scatter(x=indices, y=pressures, mode="lines+markers", name="Ciśnienie (hPa)"))

    fig.update_layout(
        title="Wykres temperatury i ciśnienia",
        xaxis_title="Numer pomiaru",
        yaxis_title="Wartości",
        legend_title="Legenda",
    )

    return fig.to_html(full_html=False)

# Endpoint do odbierania danych
@route('/data', method='POST')
def receive_data():
    data = request.json
    if not data or "temperature" not in data or "pressure" not in data:
        return {"status": "error", "message": "Nieprawidłowe dane"}

    temperature = data["temperature"]
    pressure = data["pressure"]

    save_data(temperature, pressure)
    return {"status": "success", "message": "Dane zapisane"}

# Endpoint do wyświetlania wykresu
@route('/plot')
def plot():
    plot_html = generate_plot()
    return f"""
    <html>
        <head><title>Wykres</title></head>
        <body>
            <h1>Wykres temperatury i ciśnienia</h1>
            {plot_html}
        </body>
    </html>
    """

# Endpoint do obsługi statycznych plików (np. stylów CSS, jeśli dodasz)
@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')

# Uruchomienie serwera
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
