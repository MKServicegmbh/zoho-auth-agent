from flask import Flask, redirect, request
import requests

app = Flask(__name__)

# Deine festen Zugangsdaten
CLIENT_ID = "1000.PZ8O3E1I0LJVW5GKZ7CO2VLCT20ABU"
CLIENT_SECRET = "z0fc3a0f1d5bc0ed2796b748f195a96cf8e9a1b16b"
REDIRECT_URI = "https://zoho-auth-agent.onrender.com/auth/callback"
REFRESH_TOKEN = "1000.e200305aec21fa5acfdc61cc1125b645.f84471a03912d81e594d3fb97c239054"
BASE_URL = "https://www.zohoapis.eu"

@app.route('/')
def index():
    return 'Zoho Auth Agent läuft.'

@app.route('/start-auth')
def start_auth():
    auth_url = (
        f"https://accounts.zoho.eu/oauth/v2/auth?"
        f"scope=ZohoCRM.modules.ALL,ZohoCRM.users.READ,ZohoCRM.settings.fields.ALL,ZohoBooks.fullaccess.all&"
        f"client_id={CLIENT_ID}&response_type=code&access_type=offline&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    if not code:
        return "Fehler: Kein Code erhalten."

    token_url = f"{BASE_URL}/oauth/v2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    response = requests.post(token_url, data=data)
    return response.json()

def get_access_token():
    token_url = f"{BASE_URL}/oauth/v2/token"
    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

@app.route('/check-latest-lead')
def check_latest_lead():
    try:
        token = get_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}

        # Letzten Lead holen
        lead_response = requests.get(
            f"{BASE_URL}/crm/v2/Leads?sort_by=Created_Time&sort_order=desc&per_page=1",
            headers=headers
        )
        lead_response.raise_for_status()
        lead_data = lead_response.json()
        lead = lead_data["data"][0]
        lead_id = lead["id"]
        name = lead.get("Full_Name") or f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip()
        company = lead.get("Company", "unbekannt")
        phone = lead.get("Phone", "keine Nummer")
        email = lead.get("Email", "keine E-Mail")

        kommentar = f"Neuer Lead:\nName: {name}\nFirma: {company}\nTelefon: {phone}\nE-Mail: {email}"

        note_payload = {
            "data": [{
                "Note_Title": "Lead-Auto-Kommentar",
                "Note_Content": kommentar,
                "Parent_Id": lead_id,
                "se_module": "Leads"
            }]
        }

        note_response = requests.post(
            f"{BASE_URL}/crm/v2/Notes",
            json=note_payload,
            headers={**headers, "Content-Type": "application/json"}
        )
        note_response.raise_for_status()

        return {
            "lead_id": lead_id,
            "status": "Kommentar erfolgreich erstellt",
            "kommentar": kommentar
        }

    except Exception as e:
        return {"error": str(e)}, 500
