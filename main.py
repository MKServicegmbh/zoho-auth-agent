from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Zoho Auth starten</h1>
        <a href="https://accounts.zoho.eu/oauth/v2/auth?scope=ZohoCRM.modules.ALL,ZohoBooks.fullaccess&client_id=1000.PZ8O3E1I0LJVW5GKZ7CO2VLCT20ABU&response_type=code&access_type=offline&redirect_uri=https://zoho-auth-agent.onrender.com/callback" target="_blank">
            Jetzt autorisieren
        </a>
    '''

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "<h2>❌ Kein Code empfangen.</h2>"
    return f"<h2>✅ Authorization Code:</h2><pre>{code}</pre>"

