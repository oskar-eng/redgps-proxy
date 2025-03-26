from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Token manual generado desde Postman (válido por 6 horas)
TOKEN_MANUAL = "8JKsNtW/HT87wxaSZLIsfyEFURGYUg4BOoo6swqPm9XHCY7nKtP+34bzOO8pvK7Q"

@app.route('/activos')
def obtener_activos_con_token_manual():
    # Usar el token en una solicitud directa a getdata
    response = requests.post(
        "https://api.service24gps.com/api/v1/getdata",
        files={
            "token": (None, TOKEN_MANUAL)
        }
    )

    try:
        json_data = response.json()
    except Exception:
        return {
            "error": "La respuesta no es JSON",
            "raw": response.text
        }

    if response.status_code != 200 or json_data.get("status") != 200:
        return {
            "error": "Error al obtener unidades con token manual",
            "status": response.status_code,
            "respuesta": json_data
        }

    resultado = []
    for unidad in json_data.get("data", []):
        resultado.append({
            "unidad": unidad.get("name"),
            "imei": unidad.get("imei"),
            "bateria": unidad.get("batteryLevel"),
            "ultimo_reporte": unidad.get("lastUpdate")
        })

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()


if __name__ == "__main__":
    app.run()
