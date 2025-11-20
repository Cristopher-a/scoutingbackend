from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- importar CORS
from match import match
from pits import pits
from dashboard import dashboard

app = Flask(__name__)
CORS(app)  # <--- habilitar CORS para todas las rutas

# ---------------------------
# 1. Crear PITS / subir imagen / guardar supabase
# ---------------------------
@app.route("/pits", methods=["POST"])
def pits_route():
    body = request.json()
    print(body)
    result = pits(body) 
    return jsonify(result), 200

# ---------------------------
# 2. MATCH / guardar supabase
# ---------------------------
@app.route("/match", methods=["POST"])
def match_route():
    body = request.json()
    print(body)
    result = match(body)
    return jsonify(result), 200

# ---------------------------
# 3. DEFAULT 
# ---------------------------
@app.route("/", methods=["GET"])
def login():
    return "API is running", 200

# ---------------------------
# 4. Obtener estadísticas del torneo
# ---------------------------
@app.route("/dashboard", methods=["GET"])
def stats():
    result = dashboard()
    return jsonify(result), 200

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
