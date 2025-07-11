import os
from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

@app.route('/')
def home():
    auth_url = (
        f"https://accounts.zoho.eu/oauth/v2/auth?"
        f"scope=ZohoCRM.modules.ALL,ZohoBooks.fullaccess.all&"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"redirect_uri={REDIRECT_URI}"
    )
    return f'<a href="{auth_url}" target="_blank">Zoho Auth starten</a>'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://accounts.zoho.eu/oauth/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    response = requests.post(token_url, data=payload)
    return f"<pre>{response.text}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))