from flask import Flask, jsonify
import requests

app = Flask(__name__)

# === CREDENCIALES DE REDGPS ===
API_KEY = "c95d7f74eccb5702a620011f128f750e"
USERNAME = "Olaurente"
PASSWORD = "123456789"

@app.route('/activos')
def obtener_activos():
    # 1. Obtener token automáticamente
    token_response = requests.post(
        "https://api.service24gps.com/api/v1/gettoken",
        files={
            "apikey": (None, API_KEY),
            "token": (None, ""),
            "username": (None, USERNAME),
            "password": (None, PASSWORD)
        }
    )

    try:
        token_data = token_response.json()
    except Exception:
        return {"error": "Respuesta inválida del token", "respuesta": token_response.text}

    if token_response.status_code != 200 or token_data.get("status") != 200:
        return {"error": "Error al obtener token", "respuesta": token_data}

    token = token_data.get("data")

    # 2. Llamar a getdata con token nuevo y campos requeridos
    data_response = requests.post(
        "https://api.service24gps.com/api/v1/getdata",
        files={
            "apikey": (None, API_KEY),
            "token": (None, token),
            "UseUTCDate": (None, "0"),
            "sensores": (None, "1")
        }
    )

    try:
        json_data = data_response.json()
    except Exception:
        return {"error": "Respuesta inválida del getdata", "respuesta": data_response.text}

    if data_response.status_code != 200 or json_data.get("status") != 200:
        return {"error": "Error al obtener datos de unidades", "respuesta": json_data}

    resultado = []
    for unidad in json_data.get("data", []):
        resultado.append({
            "unidad": unidad.get("UnitId"),
            "imei": unidad.get("GpsIdentif"),
            "bateria": unidad.get("BateriaGps"),
            "ultimo_reporte": unidad.get("ReportDate")
        })

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()

