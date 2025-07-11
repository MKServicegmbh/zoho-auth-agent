import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Deine Zoho-Zugangsdaten
client_id = "1000.PZ8O3E1I0LJVW5GKZ7CO2VLCT20ABU"
client_secret = "552fa43b9619dfc0f2315fbae5553881a935a57998"
redirect_uri = "https://zoho-auth-agent.onrender.com/callback"

@app.route('/')
def home():
    auth_url = (
        f"https://accounts.zoho.eu/oauth/v2/auth?"
        f"scope=ZohoCRM.modules.ALL,ZohoBooks.fullaccess.all&"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"redirect_uri={redirect_uri}"
    )
    return f'<a href="{auth_url}" target="_blank">Zoho Auth starten</a>'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://accounts.zoho.eu/oauth/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }
    response = requests.post(token_url, data=payload)
    return f"<pre>{response.text}</pre>"

# Für Render wichtig: Port 10000 vermeiden, Standard 0.0.0.0:10000 geht hier nicht
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
