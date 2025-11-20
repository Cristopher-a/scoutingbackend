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
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
