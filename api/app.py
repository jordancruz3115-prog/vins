from flask import Flask, request, render_template, abort
import os
import traceback

# get admin password from env
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


@app.route("/adminvinc684833", methods=["GET", "POST"])
def admin():
    # if password not configured, block access
    if not ADMIN_PASSWORD:
        return "Admin password not configured", 500

    # handle password submit
    if request.method == "POST":
        password = request.form.get("password")

        if password != ADMIN_PASSWORD:
            return render_template("admin_login.html", error="Invalid password")

        # correct password → load data
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

    # GET request → show login page
    return render_template("admin_login.html")
from flask import Flask, request, render_template, abort
import os
import traceback

# get admin password from env
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


@app.route("/adminvinc684833", methods=["GET", "POST"])
def admin():
    # if password not configured, block access
    if not ADMIN_PASSWORD:
        return "Admin password not configured", 500

    # handle password submit
    if request.method == "POST":
        password = request.form.get("password")

        if password != ADMIN_PASSWORD:
            return render_template("admin_login.html", error="Invalid password")

        # correct password → load data
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

    # GET request → show login page
    return render_template("admin_login.html")
