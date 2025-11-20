# dashboard_service.py

import os
from supabase_client import supabase
from openai import OpenAI

# -------------------------------
# Configuración Supabase + IA
# -------------------------------
client = OpenAI(api_key="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")

# -------------------------------
# FUNCIÓN PRINCIPAL (SIN ARGS)
# -------------------------------
def dashboard():

    # -------------------------------------------
    # 1. Obtener TODOS los pits
    # -------------------------------------------
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
    return ranking
