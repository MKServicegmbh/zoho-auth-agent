import os
from flask import Flask, request
import requests

app = Flask(__name__)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")

# Erforderlicher Scope für CRM-Nutzerinfos + Module + Zoho Books
scope = "ZohoCRM.modules.ALL ZohoCRM.users.READ ZohoCRM.settings.fields.ALL ZohoBooks.fullaccess.all"

@app.route('/')
def home():
    auth_url = (
        f"https://accounts.zoho.eu/oauth/v2/auth?"
        f"scope={scope}&"
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
    return f"<h3>Access Token Antwort:</h3><pre>{response.text}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

