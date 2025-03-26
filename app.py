from flask import Flask, jsonify
import requests

app = Flask(__name__)

# === CREDENCIALES DE REDGPS ===
API_KEY = "c95d7f74eccb5702a620011f128f750e"
USERNAME = "Olaurente"
PASSWORD = "123456789"

@app.route('/token')
def obtener_token_directo():
    token_response = requests.post(
        "https://api.service24gps.com/api/v1/gettoken",
        files={
            "apikey": (None, API_KEY),
            "token": (None, ""),
            "username": (None, USERNAME),
            "password": (None, PASSWORD)
        }
    )

    return jsonify(token_response.json())

@app.route('/activos')
def obtener_activos():
    # 1. Obtener token directamente desde la ruta completa
    token_response = requests.post(
        "https://api.service24gps.com/api/v1/gettoken",
        files={
            "apikey": (None, API_KEY),
            "token": (None, ""),
            "username": (None, USERNAME),
            "password": (None, PASSWORD)
        }
    )

    if token_response.status_code != 200:
        return jsonify({"error": "Error al obtener token", "status": token_response.status_code})

    token_data = token_response.json()
    if token_data.get("status") != 200:
        return jsonify({"error": "Respuesta sin token válido", "detalles": token_data})

    token = token_data.get("data")

    # 2. Consultar unidades usando el token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    data_response = requests.get("https://api.service24gps.com/api/v1/getunits", headers=headers)

    if data_response.status_code != 200:
        return jsonify({"error": "Error al obtener unidades", "status": data_response.status_code})

    unidades = data_response.json().get("data", [])

    resultado = []
    for unidad in unidades:
        resultado.append({
            "unidad": unidad.get("name"),
            "imei": unidad.get("imei"),
            "bateria": unidad.get("batteryLevel"),
            "ultimo_reporte": unidad.get("lastUpdate")
        })

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()
