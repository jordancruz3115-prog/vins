from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate and create the service object
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document by its name
sheet = client.open('Your_Spreadsheet_Name').sheet1

def add_data_to_sheet(name, number):
    """Add data to the Google Sheet."""
    row = [name, number]
    index = 2  # Assuming we start writing from the third row (index 2)
    sheet.insert_row(row, index)

@app.route('/add_tigo.php', methods=['POST'])
def add_data():
    name = request.form['nambari']
    number = request.form['siri']

    add_data_to_sheet(name, number)
    return "Data added successfully."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)