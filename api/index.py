from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- importar CORS
from match import match
from pits import pits
from dashboard import dashboard
from supabase import create_client, Client
from openai import OpenAI
import cloudinary
import cloudinary.uploader

# Configura Cloudinary antes de usar
cloudinary.config(
    cloud_name="djlskhtyf",
    api_key="596625527778167",
    api_secret="zTTEjWP4apxgFF8a-kYNRTzT_XY"
)
# -------------------------------
# Configuración Supabase + IA
# -------------------------------
client = OpenAI(api_key="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")

SUPABASE_URL = "https://rhttqmtzcmwilzshnxwq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJodHRxbXR6Y213aWx6c2hueHdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1OTUwOTAsImV4cCI6MjA3OTE3MTA5MH0.8dYvM8CBEdqiF9ZZhaYRKhtOin_wYGf4JYrmTTIsX74"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)  # <--- habilitar CORS para todas las rutas
@app.route("/", methods=["GET"])
def login():
    return "API is running", 200

# ---------------------------
# 1. Crear PITS / subir imagen / guardar supabase
# ---------------------------
@app.route("/pits", methods=["POST"])
def pits_route():
    body = request.json()
    region= body.get("region")
    traction_type= body.get("traction_type")
    specialty= body.get("specialty")
    team_number= body.get("team_number")
    battery_number= body.get("battery_number")
    robot_image= body.get("robot_image")
    strategy_image= body.get("strategy_image")
    strategy_comment= body.get("strategy_comment")
    robot_url = None
    strategy_url = None

    if robot_image:
        robot_url = cloudinary.uploader.upload(robot_image).get("secure_url")

    if strategy_image:
        strategy_url = cloudinary.uploader.upload(strategy_image).get("secure_url")

    data= {
        "region": region,
        "traction_type": traction_type,
        "specialty": specialty,
        "team_number": team_number,
        "battery_number": battery_number,
        "robot_image": robot_url,
        "strategy_image": strategy_url,
        "strategy_comment": strategy_comment
    }

    response = supabase.table("pits").insert(data).execute()
    return jsonify(response),200
    

# ---------------------------
# 2. MATCH / guardar supabase
# ---------------------------
@app.route("/match", methods=["POST"])
def match_route():
    body = request.json()
    team_number= body.get("team_number")
    match_number= body.get("match_number")
    regional= body.get("regional")
    check_inicio= body.get("check_inicio")
    count_motiv= body.get("count_mottif")
    count_in_cage_auto= body.get("count_in_cage_auto")
    count_out_cage_auto= body.get("count_out_cage_auto")
    count_in_cage_teleop= body.get("count_in_cage_teleop")
    count_out_cage_teleop= body.get("count_out_cage_teleop")
    count_rp= body.get("count_rp")
    check_scoring= body.get("check_scoring")
    count_in_cage_endgame= body.get("count_in_cage_endgame")    
    count_out_cage_endgame= body.get("count_out_cage_endgame")
    check_full_park= body.get("check_full_park")
    check_partial_park= body.get("check_partial_park")
    check_high= body.get("check_high")
    robot_rating= body.get("robot_rating")
    comment_robot= body.get("comment_robot")
    driver_rating= body.get("driver_rating")
    comment_driver= body.get("comment_driver")
    general_rating= body.get("general_rating")
    comment_general= body.get("comment_general")
    data  ={
        "team_number": team_number,
        "match_number": match_number,
        "regional": regional,

        "check_inicio": check_inicio*3,
        "count_motiv": count_motiv*2,
        "count_in_cage_auto": count_in_cage_auto*3,
        "count_out_cage_auto": count_out_cage_auto*1,

        "count_in_cage_teleop": count_in_cage_teleop*3,
        "count_out_cage_teleop": count_out_cage_teleop*1,
        "count_rp": count_rp,

        "check_scoring": check_scoring,
        "count_in_cage_endgame": count_in_cage_endgame*3,
        "count_out_cage_endgame": count_out_cage_endgame*1,
        "check_full_park": 10 if check_full_park  =="Sí" else 0,
        "check_partial_park": 5 if check_partial_park  =="Sí" else 0,
        "check_high": 10 if check_high == "Sí" else 0,

        "robot_rating": robot_rating,
        "comment_robot": comment_robot,
        "driver_rating": driver_rating,
        "comment_driver": comment_driver,
        "general_rating": general_rating,
        "comment_general": comment_general
    }

    response = supabase.table("matches").insert(data).execute()
    return jsonify(response), 200

# ---------------------------
# 3. DEFAULT 
# ---------------------------

# ---------------------------
# 4. Obtener estadísticas del torneo
# ---------------------------
@app.route("/dashboard", methods=["GET"])
def stats():
    pits = supabase.table("pits").select("*").execute().data
    if not pits:
        return {"error": "No pits data found"}

    # -------------------------------------------
    # 2. Obtener TODOS los matches
    # -------------------------------------------
    matches = supabase.table("matches").select("*").execute().data

    # Diccionario de matches por team_number
    matches_by_team = {}
    for m in matches:
        t = m["team_number"]
        if t not in matches_by_team:
            matches_by_team[t] = []
        matches_by_team[t].append(m)

    # Diccionario de matches por region
    matches_by_region = {}
    for m in matches:
        r = m["regional"]
        if r not in matches_by_region:
            matches_by_region[r] = []
        matches_by_region[r].append(m)

    # -------------------------------------------
    # 3. Evaluar cada equipo con IA
    # -------------------------------------------
    ranking = []

    for pit in pits:
        team_number = pit["team_number"]
        team_region = pit["region"]

        # Matches solo del mismo equipo Y mismo regional
        team_matches = [
            m for m in matches_by_team.get(team_number, [])
            if m["regional"] == team_region
        ]

        # Matches de toda la región (contexto)
        region_matches = matches_by_region.get(team_region, [])

        prompt = f"""
Eres un analista experto de FIRST Robotics Competition.

Evalúa al siguiente equipo usando la información dada:

PITS:
{pit}

MATCHES DEL EQUIPO (MISMO REGIONAL):
{team_matches}

MATCHES DE LA REGIÓN (contexto):
{region_matches}

Evalúa del 1 al 5 basado en:
- Diseño técnico del robot
- Capacidad ofensiva/defensiva
- Autonomía
- Teleoperado
- Consistencia entre partidos
- Confiabilidad general

Responde SOLAMENTE en formato JSON:
{{
  "score": número entre 1 y 5,
  "analysis": "explicación corta"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Intentar convertir la respuesta
        try:
            result = eval(response.choices[0].message.content)
        except:
            result = {"score": 0, "analysis": "Invalid AI response"}

        ranking.append({
            "team_number": team_number,
            "region": team_region,
            "pit": pit,
            "matches": team_matches,
            "score": result.get("score", 0),
            "analysis": result.get("analysis", "")
        })

    # -------------------------------------------
    # 4. Ordenar de mejor a peor por score global
    # -------------------------------------------
    ranking.sort(key=lambda x: x["score"], reverse=True)

    # -------------------------------------------
    # 5. Retornar el ranking final
    # -------------------------------------------
 

    return jsonify(ranking), 200

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
