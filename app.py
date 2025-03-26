from flask import Flask, jsonify
import requests

app = Flask(__name__)

# === CREDENCIALES Y TOKEN FIJO ===
API_KEY = "c95d7f74eccb5702a620011f128f750e"
TOKEN_MANUAL = "8JKsNtW/HT87wxaSZLIsfyEFURGYUg4BOoo6swqPm9XHCY7nKtP+34bzOO8pvK7Q"

@app.route('/activos')
def obtener_activos_con_token_fijo():
    # Enviar token generado desde Postman + campos correctos
    data_response = requests.post(
        "https://api.service24gps.com/api/v1/getdata",
        files={
            "apikey": (None, API_KEY),
            "token": (None, TOKEN_MANUAL),
            "UseUTCDate": (None, "0"),
            "sensores": (None, "1")
        }
    )

    try:
        json_data = data_response.json()
    except Exception:
        return jsonify({"error": "Respuesta no es JSON", "raw": data_response.text})

    if data_response.status_code != 200 or json_data.get("status") != 200:
        return jsonify({
            "error": "Error en respuesta getdata",
            "status": data_response.status_code,
            "respuesta": json_data
        })

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

