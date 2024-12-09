from bottle import route, run, static_file
import json
import os
import plotly.graph_objects as go

# Ścieżka do pliku z danymi
DATA_FILE = "sensor_data.json"

def read_data():
    """
    Odczytuje dane z pliku JSON.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def generate_plot():
    """
    Generuje wykres na podstawie danych z pliku JSON.
    """
    data = read_data()
    if not data:
        return "<h3>Brak danych do wyświetlenia.</h3>"

    timestamps = [entry["timestamp"] for entry in data]
    temperatures = [entry["temperature"] for entry in data]
    humidities = [entry["humidity"] for entry in data]

    # Tworzenie wykresu
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperatura (°C)'))
    fig.add_trace(go.Scatter(x=timestamps, y=humidities, mode='lines+markers', name='Wilgotność (%)'))

    fig.update_layout(
        title="Wykres temperatury i wilgotności",
        xaxis_title="Czas",
        yaxis_title="Wartości",
        legend_title="Parametry",
        xaxis=dict(tickangle=45),
        template="plotly_white"
    )

    return fig.to_html(full_html=False)

@route("/")
def index():
    """
    Wyświetla stronę główną z wykresem.
    """
    plot_html = generate_plot()
    return f"""
    <html>
        <head><title>Wykres danych z czujnika</title></head>
        <body>
            <h1>Dane z czujnika DHT11</h1>
            {plot_html}
        </body>
    </html>
    """

@route('/static/<filename:path>')
def server_static(filename):
    """
    Obsługuje statyczne pliki, jeśli potrzebne (np. CSS).
    """
    return static_file(filename, root='./static')

# Uruchomienie serwera
if __name__ == "__main__":
    run(host="192.168.109.91", port=8080, debug=True)
