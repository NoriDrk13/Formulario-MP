from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# -------------------------
# GOOGLE SHEETS
# -------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json
import os

google_creds = json.loads(
    os.environ["GOOGLE_CREDENTIALS"]
)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds,
    scope
)

client = gspread.authorize(creds)

sheet = client.open("Formulario Registros").sheet1

# -------------------------
# PRODUCTOS
# -------------------------

PRODUCTOS_FILE = "Productos.xlsx"

# -------------------------
# PAGINA PRINCIPAL
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------
# BUSCAR DESCRIPCION
# -------------------------

@app.route("/buscar_descripcion/<codigo>")
def buscar_descripcion(codigo):

    df = pd.read_excel(PRODUCTOS_FILE, dtype=str)

    producto = df[df["codigo"].astype(str) == str(codigo)]

    if not producto.empty:

        descripcion = producto.iloc[0]["descripcion"]

        return jsonify({
            "descripcion": descripcion
        })

    return jsonify({
        "descripcion": ""
    })

# -------------------------
# GUARDAR REGISTRO
# -------------------------

@app.route("/guardar", methods=["POST"])
def guardar():

    data = request.json

    fila = [

        data["codigo"],
        data["descripcion"],
        data["cantidad"],
        data["numero_guia"],
        data["observaciones"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ]

    sheet.append_row(fila)

    return jsonify({
        "mensaje": "Registro guardado correctamente"
    })

# -------------------------

if __name__ == "__main__":
    app.run(debug=True)