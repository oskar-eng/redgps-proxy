from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.service24gps.com/api/v1"
API_KEY = "c95d7f74eccb5702a620011f128f750e"
USERNAME = "Olaurente"
PASSWORD = "123456789"

@app.route('/activos')
def obtener_activos():
   token_response = requests.post(
    f"{API_URL}/gettoken",
    files={
        "apikey": (None, API_KEY),
        "username": (None, USERNAME),
        "password": (None, PASSWORD)
    }
)
    })

    if token_response.status_code != 200:
        return jsonify({"error": "Error al obtener token", "status": token_response.status_code})

    token = token_response.json().get("data")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data_response = requests.get(f"{API_URL}/getunits", headers=headers)

    if data_response.status_code != 200:
        return jsonify({"error": "Error al obtener unidades", "status": data_response.status_code})

    unidades = data_response.json().get("data", [])

    resultado = []
    for u in unidades:
        resultado.append({
            "unidad": u.get("name"),
            "imei": u.get("imei"),
            "bateria": u.get("batteryLevel"),
            "ultimo_reporte": u.get("lastUpdate")
        })

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()
